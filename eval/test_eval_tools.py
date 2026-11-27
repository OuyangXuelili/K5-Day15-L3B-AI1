"""Test cho diagnose.py, build_benchmark_v2.py --verify và hợp đồng lời hướng dẫn an toàn.
Các ca lấy từ ba lượt review độc lập ngày 27/11. Chỉ dùng thư mục tạm, không ghi vào repo, không gọi API.
Chạy: python eval/test_eval_tools.py"""
import csv, json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
# Ép tiến trình con xuất UTF-8 và đọc lại bằng UTF-8 — Python Windows mặc định dùng CP1252 (review vòng 4).
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", MODEL_PROVIDER="fake", PYTHONUTF8="1", PYTHONIOENCODING="utf-8")


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=ROOT)


def make_run(tmp, mutate_trace=None, run_id="SIM"):
    """Lượt giả lập trên bản nháp: model = regex preview. → (đường dẫn CSV, đường dẫn trace)."""
    code = r'''
import csv, json, sys, os
sys.path[:0] = ["codebase", "eval"]; os.environ["MODEL_PROVIDER"] = "fake"
import tracing, agent
rows = list(csv.DictReader(open("eval/benchmark.csv", encoding="utf-8-sig")))
out, tr = [], []
for r in rows:
    tracing.begin(r["id"]); res = agent.answer(r["input"]); _, ev = tracing.end()
    out.append({"run_id": sys.argv[2], **r, "output": res["output"], "error": "", "model": "fake", "model_calls": "1"})
    tr += [{"run_id": sys.argv[2], "case": r["id"], **e} for e in ev]
with open(sys.argv[1] + "/run-9.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
json.dump(tr, open(sys.argv[1] + "/trace.json", "w", encoding="utf-8"), ensure_ascii=False, default=str)
'''
    r = subprocess.run([sys.executable, "-c", code, str(tmp), run_id], capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=ROOT)
    assert r.returncode == 0, r.stderr
    events = json.loads((tmp / "trace.json").read_text(encoding="utf-8"))
    if mutate_trace:
        events = mutate_trace(events)
    (tmp / "run-9.jsonl").write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in events), encoding="utf-8")
    return tmp / "run-9.csv", tmp / "run-9.jsonl"


def set_model_output(case, text):
    def f(events):
        for e in events:
            if e.get("case") == case and e.get("kind") == "model":
                e["output"] = text
        return events
    return f


class DiagnoseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def diag(self, csv_path, trace):
        return run("eval/diagnose.py", csv_path, "--trace", trace, "--gold", "eval/benchmark-gold.json")

    def group(self, out, name):
        return next(l for l in out.splitlines() if l.strip().startswith(name)).split()[2:]

    def row_of(self, out, cid):
        return next(l for l in out.splitlines() if l.startswith("| %s |" % cid))

    def test_baseline_runs(self):
        r = self.diag(*make_run(self.tmp))
        self.assertEqual(r.returncode, 0, r.stderr); self.assertIn("Đạt 17/30", r.stdout)

    def test_trace_without_run_id_is_rejected(self):
        def strip(events):
            for e in events:
                e.pop("run_id", None)
            return events
        r = self.diag(*make_run(self.tmp, strip))
        self.assertNotEqual(r.returncode, 0); self.assertIn("run_id", r.stdout + r.stderr)

    def test_invalid_issue_and_too_many_items_are_schema_errors(self):
        r = self.diag(*make_run(self.tmp, set_model_output("D12", '{"issue": "refund_now", "item_ids": []}')))
        self.assertIn("D12", self.group(r.stdout, "ky_thuat"))
        self.assertIn("fallback", self.row_of(r.stdout, "D12"))
        seven = json.dumps({"issue": "missing_item", "item_ids": ["I0%d" % i for i in range(1, 8)]})
        r = self.diag(*make_run(self.tmp, set_model_output("D13", seven)))
        self.assertIn("item_ids không phải danh sách", self.row_of(r.stdout, "D13"))
        self.assertIn("D13", self.group(r.stdout, "ky_thuat"))

    def test_no_model_call_is_not_fallback(self):
        def drop(events):
            return [e for e in events if not (e.get("case") == "D27" and e.get("kind") == "model")]
        r = self.diag(*make_run(self.tmp, drop))
        line = self.row_of(r.stdout, "D27")
        self.assertIn("khong_goi_model", line); self.assertNotIn("fallback", line)

    def test_gold_of_other_set_is_rejected(self):
        # Lượt chạy trên một bộ có input khác nhãn vàng (vd bộ cũ v1 dùng chung id D01–D30) phải bị chặn.
        csv_path, trace = make_run(self.tmp)
        rows = list(csv.DictReader(csv_path.read_text(encoding="utf-8").splitlines()))
        rows[4]["input"] = "FD002 Đơn giao trễ đúng 30 phút, có được voucher không?"
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
        r = self.diag(csv_path, trace)
        self.assertNotEqual(r.returncode, 0); self.assertIn("không khớp", r.stdout + r.stderr)


class VerifyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for d in ("codebase", "data"):
            shutil.copytree(ROOT / d, self.tmp / d, ignore=shutil.ignore_patterns("__pycache__"))
        (self.tmp / "eval").mkdir()
        for f in ("benchmark.csv", "benchmark-gold.json", "build_benchmark_v2.py"):
            shutil.copy(ROOT / "eval" / f, self.tmp / "eval" / f)
        self.csv = self.tmp / "eval/benchmark.csv"; self.gold = self.tmp / "eval/benchmark-gold.json"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def verify(self):
        return run(self.tmp / "eval/build_benchmark_v2.py", self.tmp, "--verify")

    def rows(self):
        return list(csv.DictReader(self.csv.read_text(encoding="utf-8-sig").splitlines()))

    def write(self, rows):
        with self.csv.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    def test_clean_copy_passes(self):
        r = self.verify(); self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_extra_and_duplicate_ids_fail(self):
        rows = self.rows(); self.write(rows + [dict(rows[0], id="D99")])
        self.assertNotEqual(self.verify().returncode, 0)
        self.write(rows + [rows[0]])
        self.assertNotEqual(self.verify().returncode, 0)

    def test_expected_formatting_only_is_ok_but_value_change_fails(self):
        rows = self.rows()
        rows[0]["expected"] = json.dumps(json.loads(rows[0]["expected"]), ensure_ascii=False, indent=2)
        self.write(rows); self.assertEqual(self.verify().returncode, 0, self.verify().stdout)
        e = json.loads(rows[0]["expected"]); e["amount_vnd"] += 1; rows[0]["expected"] = json.dumps(e)
        self.write(rows); self.assertNotEqual(self.verify().returncode, 0)

    def test_gold_label_change_fails(self):
        g = json.loads(self.gold.read_text(encoding="utf-8")); g[15]["gold_item_ids"] = ["I01"]
        self.gold.write_text(json.dumps(g, ensure_ascii=False), encoding="utf-8")
        r = self.verify(); self.assertNotEqual(r.returncode, 0); self.assertIn("nhãn vàng lệch", r.stdout)


class SafetyContractTest(unittest.TestCase):
    def test_food_safety_reason_tells_to_stop_and_call_115(self):
        sys.path.insert(0, str(ROOT / "codebase"))
        import tools
        for oid in ("FD007", "FD011", "FD017", None):
            r = tools.check_limit(tools.get_order(oid) if oid else None, "food_safety", [])
            self.assertEqual((r["decision"], r["policy_id"], r["urgent"], r["amount_vnd"]), ("handoff", "P07", True, 0))
            self.assertIn("Ngừng dùng món", r["reason"]); self.assertIn("115", r["reason"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
