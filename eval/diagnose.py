"""Chẩn đoán một lượt eval theo từng bước của workflow, để phân tích lỗi (R5). Chỉ đọc, không sửa file nào.

Với mỗi câu, so lời model trả (đọc từ traces/run-N.jsonl) với nhãn vàng, rồi xếp câu trượt vào ĐÚNG MỘT nhóm:
  ky_thuat    lỗi gọi model, hoặc output model / output cuối sai schema (cùng quy tắc với agent.py)
  phan_loai   model chọn sai loại sự cố (issue) và luồng sau không sửa lại được
  nhan_mon    đúng loại sự cố nhưng sai danh sách món (item_ids)
  sau_model   model đúng (hoặc đã được hàng rào sửa đúng, hoặc không gọi model), kết quả cuối vẫn sai → lỗi ở code
Ghi rõ lý do issue bị đổi sau model: an_toan (regex an toàn), nhieu_ma_don, fallback (output model sai schema),
khong_goi_model (câu không có lời gọi model nào).
In riêng các điều kiện cứng: trả thừa, vượt trần, tiền sai kiểu, giao dịch thật, câu tu_choi trượt, câu an toàn trượt.

Nhãn vàng phải KHỚP đúng bộ câu thử của lượt chạy: script so ô input của từng câu với input trong file nhãn vàng
và dừng nếu lệch (bộ cũ và bản nháp dùng chung id D01–D30 cho nội dung khác nhau).

Chạy: python eval/diagnose.py eval/run-1.csv [--gold eval/benchmark-gold.json] [--trace traces/run-1.jsonl]
"""
import argparse, csv, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "eval"), str(ROOT / "codebase")]
from grade import failures, HARD  # noqa: E402
from tools import order_ids, redact, safety_issue  # noqa: E402

GROUPS = ("ky_thuat", "phan_loai", "nhan_mon", "sau_model")


def load_trace(path):
    """→ (case id → [output model], tập run_id trong trace)."""
    out, run_ids = {}, set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if e.get("run_id"):
            run_ids.add(e["run_id"])
        if e.get("kind") == "model":
            out.setdefault(e.get("case"), []).append(e.get("output") or "")
    return out, run_ids


def _agent_rules():
    """Đọc ISSUES và giới hạn số món từ codebase/agent.py (không import để khỏi nạp .env) — luôn khớp agent."""
    import ast, re
    src = (ROOT / "codebase" / "agent.py").read_text(encoding="utf-8")
    issues = None
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "ISSUES" for t in node.targets):
            issues = set(ast.literal_eval(node.value))
    m = re.search(r"len\(items\)\s*>\s*(\d+)", src)
    if not issues or not m:
        sys.exit("Không đọc được ISSUES / giới hạn số món trong codebase/agent.py — cập nhật diagnose.py.")
    return issues, int(m.group(1))


ISSUES, MAX_ITEMS = _agent_rules()


def parse_model(raw):
    """→ (issue, item_ids đã sắp xếp, lỗi schema | None, có gọi model không). Cùng quy tắc với agent.py:
    output sai các quy tắc này thì agent coi là unclear (fallback)."""
    if not raw:
        return None, None, None, False
    try:
        m = json.loads(raw[-1])
    except ValueError:
        return None, None, "output model không phải JSON (có thể bị cắt trong trace)", True
    if not isinstance(m, dict) or m.get("issue") not in ISSUES:
        return None, None, "issue không thuộc danh sách hợp lệ của agent", True
    items = m.get("item_ids", [])
    if not isinstance(items, list) or len(items) > MAX_ITEMS or any(not isinstance(i, str) for i in items):
        return m["issue"], None, "item_ids không phải danh sách ≤%d chuỗi" % MAX_ITEMS, True
    return m["issue"], sorted(items), None, True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run", type=Path)
    ap.add_argument("--gold", type=Path)
    ap.add_argument("--trace", type=Path)
    a = ap.parse_args()
    gold_path = a.gold or next((p for p in (ROOT / "eval/benchmark-gold.json",) if p.exists()), None)
    if not gold_path:
        sys.exit("Không thấy file nhãn vàng; truyền --gold")
    gold = {g["id"]: g for g in json.loads(gold_path.read_text(encoding="utf-8"))}
    rows = list(csv.DictReader(a.run.open(encoding="utf-8-sig")))

    # 1. Ghép nhãn vàng theo NỘI DUNG, không chỉ theo id.
    bad = [r["id"] for r in rows if r["id"] not in gold or gold[r["id"]].get("input") != r["input"]]
    if bad:
        sys.exit("Nhãn vàng %s không khớp bộ câu thử của lượt này ở: %s. Dùng đúng file nhãn vàng của bộ đã chạy."
                 % (gold_path.name, ", ".join(bad[:10])))
    # 2. Trace phải của đúng lượt này.
    trace = a.trace or ROOT / "traces" / (a.run.stem + ".jsonl")
    if not trace.exists():
        sys.exit("Không thấy trace %s" % trace)
    models, trace_ids = load_trace(trace)
    csv_ids = {r.get("run_id") or "" for r in rows}
    if len(csv_ids) != 1 or "" in csv_ids:
        sys.exit("CSV phải có đúng một run_id, có ở mọi dòng (đang có %s) — không ghép." % sorted(csv_ids))
    if trace_ids != csv_ids:
        sys.exit("run_id của trace %s khác CSV %s, hoặc trace thiếu run_id — không ghép." % (sorted(trace_ids), sorted(csv_ids)))

    groups = {k: [] for k in GROUPS}
    hard = {k: [] for k in HARD + ("tu_choi_truot", "an_toan_truot")}
    table = []
    for r in rows:
        cid, g = r["id"], gold[r["id"]]
        fails = failures(r)
        m_issue, m_items, schema_err, called = parse_model(models.get(cid))
        try:
            out = json.loads(r["output"])
            final_issue = out.get("issue") if isinstance(out, dict) else None
        except (ValueError, TypeError):
            out, final_issue = None, None
        text = redact(r["input"].strip())
        why = []
        if not called:
            why.append("khong_goi_model")      # vd hàng rào chặn trước khi gọi model
        elif schema_err:
            why.append("fallback")             # agent.py coi output sai schema là unclear
        if final_issue and final_issue != m_issue:
            if safety_issue(text):
                why.append("an_toan")
            if len(order_ids(text)) > 1:
                why.append("nhieu_ma_don")
            if m_issue and not why:
                why.append("khac")
        if fails:
            if "technical_error" in fails or schema_err or not isinstance(out, dict):
                grp = "ky_thuat"
            elif not called:
                grp = "sau_model"   # không gọi model: code/hàng rào tự quyết, lỗi thuộc phần code
            elif final_issue != g["gold_issue"] and m_issue != g["gold_issue"]:
                grp = "phan_loai"
            elif g["gold_issue"] in ("missing_item", "wrong_item") and m_items != sorted(g["gold_item_ids"]):
                grp = "nhan_mon"
            else:
                grp = "sau_model"   # model đúng, hoặc hàng rào đã sửa đúng issue mà kết quả vẫn sai
            groups[grp].append(cid)
            for k in HARD:
                if k in fails:
                    hard[k].append(cid)
            if r.get("type") == "tu_choi":
                hard["tu_choi_truot"].append(cid)
            if g["gold_issue"] == "food_safety":
                hard["an_toan_truot"].append(cid)
        table.append((cid, r.get("type", ""), "đạt" if not fails else "TRƯỢT", g["gold_issue"], m_issue or "—",
                      final_issue or "—", ",".join(why), schema_err or "", ",".join(fails)))

    ok = sum(1 for t in table if t[2] == "đạt")
    print("Lượt %s · run_id %s · nhãn vàng %s · trace %s" % (a.run.name, ",".join(sorted(csv_ids)) or "—", gold_path.name, trace.name))
    print("Đạt %d/%d" % (ok, len(rows)))
    for k in GROUPS:
        print("  %-10s %2d  %s" % (k, len(groups[k]), " ".join(groups[k])))
    print("Điều kiện cứng: " + " · ".join("%s %d%s" % (k, len(v), (" (" + " ".join(v) + ")") if v else "") for k, v in hard.items()))
    print("\n| id | type | kết quả | issue vàng | issue model | issue cuối | vì sao đổi | lỗi schema | nhãn lỗi chấm |")
    print("|---|---|---|---|---|---|---|---|---|")
    for t in table:
        print("| %s |" % " | ".join(str(x) for x in t))


if __name__ == "__main__":
    main()
