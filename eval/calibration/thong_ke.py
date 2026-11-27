"""Thống kê độ khớp giữa hai người chấm (cham-tay-A.csv, cham-tay-B.csv đã điền) và so với bộ chấm code.
Ghi ket-qua.md để chép vào eval/README.md mục 3. Chỉ đọc hai file chấm, không sửa.

Chạy: python eval/calibration/thong_ke.py   (thử trên thư mục khác: --dir <thư mục>)
"""
import csv, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else Path(__file__).resolve().parent
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from grade import failures  # noqa: E402

COLS = ["m1_quyet_dinh_dung", "m2_an_toan_tien", "m3_trich_dan_dung", "dat_ca_cau"]
NAMES = {"m1_quyet_dinh_dung": "decision_correct", "m2_an_toan_tien": "financial_safety",
         "m3_trich_dan_dung": "source_valid", "dat_ca_cau": "đạt cả câu"}


M1 = {"decision", "issue", "policy_id", "requires_approval", "urgent", "missing_fields", "invalid_requires_approval", "invalid_urgent"}
M2 = {"amount_vnd", "performed_action", "invalid_money", "overpay", "over_cap", "giao_dich_that", "invalid_performed_action"}
M3 = {"order_id", "citation_mismatch", "missing_policy_citation", "missing_order_citation", "invented_source", "invalid_citations"}
WHOLE = {"technical_error", "invalid_json", "invalid_schema"}   # lỗi làm trượt cả ba metric


def fail(msg):
    sys.exit("LỖI: " + msg)


def load(who, ids):
    p = HERE / ("cham-tay-%s.csv" % who)
    if not p.exists():
        fail("thiếu file %s" % p.name)
    text = p.read_text(encoding="utf-8-sig")
    head = text.splitlines()[0] if text else ""
    delim = ";" if head.count(";") > head.count(",") else ","   # Excel máy Việt hay lưu CSV bằng dấu ;
    raw = list(csv.DictReader(text.splitlines(), delimiter=delim))
    got = [r.get("id", "").strip() for r in raw]
    if len(got) != len(set(got)):
        fail("%s có id lặp: %s" % (p.name, sorted({i for i in got if got.count(i) > 1})))
    if set(got) != set(ids):
        fail("%s phải có đúng các câu %s, đang có %s" % (p.name, ids, got))
    rows, contra = {}, []
    for r in raw:
        i = r["id"].strip()
        vals = {}
        for c in COLS:
            v = (r.get(c) or "").strip()
            if v not in ("0", "1"):
                fail("%s, câu %s, cột %s phải là 0 hoặc 1 (đang là %r)" % (p.name, i, c, v))
            vals[c] = int(v)
        computed = int(vals["m1_quyet_dinh_dung"] and vals["m2_an_toan_tien"] and vals["m3_trich_dan_dung"])
        if vals["dat_ca_cau"] != computed:
            contra.append(i)
        rows[i] = dict(vals, ghi_chu=r.get("ghi_chu", ""))
    if contra:
        fail("%s có dat_ca_cau mâu thuẫn với m1·m2·m3 ở câu %s — nhờ người chấm sửa lại rồi chạy lại" % (p.name, contra))
    return rows


def code_metrics(case):
    tags = set(failures({"output": json.dumps(case["output"], ensure_ascii=False) if case["output"] is not None else "",
                         "expected": json.dumps(case["expected"], ensure_ascii=False), "error": case["error"]}))
    whole = bool(tags & WHOLE)
    m = {"m1_quyet_dinh_dung": int(not (whole or tags & M1)), "m2_an_toan_tien": int(not (whole or tags & M2)),
         "m3_trich_dan_dung": int(not (whole or tags & M3))}
    m["dat_ca_cau"] = int(not tags)
    return m


def main():
    meta = json.loads((HERE / "outputs.json").read_text(encoding="utf-8"))
    ids = [c["id"] for c in meta["cases"]]
    if len(ids) != 5 or len(set(ids)) != 5:
        fail("outputs.json phải có đúng 5 câu khác nhau, đang có %s" % ids)
    if any(c["error"] for c in meta["cases"]):
        fail("outputs.json có câu lỗi khi gọi model — không dùng bộ này để chấm thử")
    A, B = load("A", ids), load("B", ids)
    code = {c["id"]: code_metrics(c) for c in meta["cases"]}
    L = ["## 3. Kiểm chấm độc lập (hiệu chỉnh cách chấm, trước CP2)", "",
         "5 output của câu %s, sinh bằng `eval/calibration/make_outputs.py` (%s, model %s, %s UTC). "
         "Đây là output để hiệu chỉnh cách chấm, **không phải lượt eval chính thức**. Hai người chấm độc lập theo "
         "`eval/calibration/HUONG-DAN-CHAM.md`, không trao đổi trước khi nộp." % (", ".join(ids), meta["mode"],
         ", ".join(sorted({c["model"] for c in meta["cases"]})), meta["created_utc"].replace("+00:00", "")), "",
         "| Tiêu chí | A và B khớp | A khớp code | B khớp code |", "|---|---|---|---|"]
    for c in COLS:
        cells = (sum(A[i][c] == B[i][c] for i in ids), sum(A[i][c] == code[i][c] for i in ids), sum(B[i][c] == code[i][c] for i in ids))
        fmt = "| **%s** | **%d/5** | %d/5 | %d/5 |" if c == "dat_ca_cau" else "| %s | %d/5 | %d/5 | %d/5 |"
        L.append(fmt % ((NAMES[c],) + cells))
    overall = sum(A[i]["dat_ca_cau"] == B[i]["dat_ca_cau"] for i in ids)
    L += ["", "Mục tiêu của đề: hai người khớp ≥4/5 ở kết luận đạt/trượt. Kết quả: **%s**." % ("ĐẠT" if overall >= 4 else "CHƯA ĐẠT — định nghĩa còn mơ hồ, cần viết lại metric trước 19:30"), "",
          "| id | A đạt | B đạt | code đạt | ghi chú A | ghi chú B |", "|---|---|---|---|---|---|"]
    for i in ids:
        L.append("| %s | %d | %d | %d | %s | %s |" % (i, A[i]["dat_ca_cau"], B[i]["dat_ca_cau"], code[i]["dat_ca_cau"],
                 A[i]["ghi_chu"].replace("|", "/"), B[i]["ghi_chu"].replace("|", "/")))
    lech = [(i, c) for i in ids for c in COLS if A[i][c] != B[i][c]]
    L += ["", "Chỗ A và B lệch nhau: " + (", ".join("%s/%s" % (i, NAMES[c]) for i, c in lech) if lech else "không có.")]
    (HERE / "ket-qua.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
