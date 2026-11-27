"""Chạy MỘT lần bộ held-out H01–H10 bằng đúng code của lượt 2, rồi chấm bằng eval/grade.py.
Không đụng eval/benchmark.csv, không tạo eval/run-N.csv (không làm lệch số lượt chính thức).
Chạy: python3 eval/heldout/run_heldout.py
  --preview   (nội bộ) chạy cùng 10 câu không gọi model, in số đạt dạng JSON."""
import csv, datetime, json, os, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
for s in (sys.stdout, sys.stderr):
    try: s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / "eval"), str(ROOT / "codebase")]
CASES, GOLD = HERE / "heldout.csv", HERE / "heldout-gold.json"
OUT, TRACE, SUMMARY = HERE / "heldout-run-1.csv", HERE / "heldout-run-1.jsonl", HERE / "heldout-summary.md"
CODE = ["codebase/agent.py", "codebase/tools.py", "codebase/ai.py", "data/policies.json", "data/orders.json"]
RUN2_COMMIT = "38d67a7"

def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True, encoding="utf-8")

def load():
    return list(csv.DictReader(CASES.open(encoding="utf-8")))

def preview():
    import agent
    from grade import failures
    res = {r["id"]: not failures({"output": agent.answer(r["input"])["output"], "expected": r["expected"], "error": ""})
           for r in load()}
    print(json.dumps(res))

def main():
    if OUT.exists():
        sys.exit("Đã có %s: bộ held-out chỉ chạy MỘT lần. Không chạy lại." % OUT.name)
    for p in ("eval/heldout/heldout.csv", "eval/heldout/heldout-gold.json", "eval/heldout/build_heldout.py"):
        if git("ls-files", "--error-unmatch", p).returncode or git("diff", "--quiet", "HEAD", "--", p).returncode:
            sys.exit("%s chưa commit hoặc đã sửa sau commit. Phải commit bộ câu + nhãn vàng TRƯỚC khi chạy." % p)
    if git("diff", "--quiet", RUN2_COMMIT, "--", *CODE).returncode:
        sys.exit("Code/dữ liệu đã khác bản chạy lượt 2 (%s). Held-out phải đo đúng code lượt 2." % RUN2_COMMIT)
    import run_eval as ev
    from grade import failures, HARD
    answer, tracing = ev.load_answer()
    rows_in, stamp = load(), datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    rid = "heldout-run-1@" + stamp
    rows, cases = [], []
    for it in rows_in:
        row, events = ev.call_case(answer, tracing, it["id"], it["input"])
        row.update(run_id=rid, id=it["id"], type=it["type"], input=it["input"], expected=it["expected"],
                   pass_criterion=it["pass_criterion"], ghi_chu="")
        tags = failures(row)
        row["pass"] = "0" if tags else "1"
        row["ghi_chu"] = ";".join(tags)
        rows.append(row)
        cases.append((it["id"], list(events) + [{"kind": "final", "output": row["output"], "error": row["error"]}]))
        print("  %s %s %s" % (it["id"], "đạt" if not tags else "trượt", ";".join(tags)))
    if ev.looks_mock(rows):
        sys.exit("Không gọi model thật (fake / token 0). Không ghi file. Kiểm .env rồi chạy lại.")
    ev.write_csv(str(OUT), ev.OUT_COLS, rows)
    with TRACE.open("w", encoding="utf-8") as f:
        for cid, evs in cases:
            for e in evs:
                f.write(json.dumps(dict({"run_id": rid, "case": cid}, **e), ensure_ascii=False, default=str) + "\n")
    env = dict(os.environ, MODEL_PROVIDER="fake")
    pv = json.loads(subprocess.run([sys.executable, __file__, "--preview"], capture_output=True, text=True,
                                   encoding="utf-8", env=env, check=True).stdout.strip().splitlines()[-1])
    gold = {g["id"]: g for g in json.loads(GOLD.read_text(encoding="utf-8"))}
    model_out = {}
    for cid, evs in cases:
        for e in evs:
            if e.get("kind") == "model":
                model_out[cid] = e.get("output", "")
    ok = [r for r in rows if not r["error"]]
    npass = sum(r["pass"] == "1" for r in rows)
    hard = {t: [r["id"] for r in rows if t in r["ghi_chu"].split(";")] for t in HARD}
    L = ["# Held-out H01–H10 — kết quả chạy một lần", "",
         "Run ID `%s` · model `%s` · code giống lượt 2 (`%s`) · bộ câu commit trước khi chạy." % (rid, rows[0]["model"], RUN2_COMMIT), "",
         "**Đạt %d/%d** · preview cùng code, không gọi model: %d/%d" % (npass, len(rows), sum(pv.values()), len(pv)), "",
         "Theo type: " + " · ".join("%s %d/%d" % (t, sum(r["pass"] == "1" for r in rows if r["type"] == t),
                                                sum(r["type"] == t for r in rows)) for t in ("thuong", "kho", "tu_choi")), "",
         "Điều kiện cứng: " + " · ".join("%s %d" % (t, len(v)) for t, v in hard.items()), "",
         "Token trung bình mỗi câu: %.0f vào / %.1f ra" % (sum(r["tokens_in"] for r in ok) / len(ok), sum(r["tokens_out"] for r in ok) / len(ok)), "",
         "| id | type | kết quả | preview | issue vàng | issue cuối | output model | nhãn lỗi |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        try: final = json.loads(r["output"]).get("issue")
        except Exception: final = "?"
        L.append("| %s | %s | %s | %s | %s | %s | `%s` | %s |" % (r["id"], r["type"], "đạt" if r["pass"] == "1" else "**trượt**",
                 "đạt" if pv.get(r["id"]) else "trượt", gold[r["id"]]["gold_issue"], final,
                 model_out.get(r["id"], "")[:90].replace("|", "/"), r["ghi_chu"]))
    SUMMARY.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[4:9]))
    print("Đã ghi %s, %s, %s." % (OUT.name, TRACE.name, SUMMARY.name))

if __name__ == "__main__":
    preview() if "--preview" in sys.argv[1:] else main()
