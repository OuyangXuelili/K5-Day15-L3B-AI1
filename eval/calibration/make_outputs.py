"""Sinh 5 output để hai người chấm thử độc lập (R4, guide 2.4 bước 4). KHÔNG phải một lượt eval.

Chạy 5 câu đã chọn của bản nháp v2 qua đúng luồng codebase/agent.py với model thật (đọc .env như bộ chạy),
ghi outputs.json (output, model, token) và hai file chấm giống hệt nhau cham-tay-A.csv, cham-tay-B.csv.
Không tạo eval/run-N.csv, không đổi số thứ tự lượt chính thức.

Chạy:  python eval/calibration/make_outputs.py            # cần .env có MODEL_PROVIDER thật
Thử:   python eval/calibration/make_outputs.py --dry-run  # chế độ fake, ghi vào thư mục tạm, không đụng repo
"""
import argparse, csv, json, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CASES = ["D06", "D14", "D20", "D26", "D29"]   # biên 31 phút · phải hỏi đúng trường (ảnh) · số lượng bằng chữ · an toàn thực phẩm · tấn công


FIELDS = ["decision", "issue", "policy_id", "amount_vnd", "requires_approval", "performed_action",
          "order_id", "urgent", "missing_fields", "citations"]


def show(d, keys, with_reason=False):
    """Hiện GIÁ TRỊ JSON GỐC (true/false/null, số, chuỗi có ngoặc kép) để người chấm thấy đúng thứ code chấm.
    Trường mà đáp án có nhưng output không có thì ghi THIẾU."""
    parts = []
    for k in keys:
        parts.append("%s: %s" % (k, json.dumps(d[k], ensure_ascii=False) if k in d else "THIẾU"))
    if with_reason and "reason" in d:
        parts.append("reason (không chấm): %s" % json.dumps(d["reason"], ensure_ascii=False))
    return " | ".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    import os
    if a.dry_run:
        os.environ["MODEL_PROVIDER"] = "fake"
    sys.path[:0] = [str(ROOT / "codebase")]
    import ai, agent, tracing                       # noqa: E402
    if ai.MODEL_PROVIDER == "fake" and not a.dry_run:
        sys.exit("MODEL_PROVIDER đang là fake. Điền .env (provider thật) rồi chạy lại, hoặc dùng --dry-run để thử.")
    out_dir = Path(tempfile.mkdtemp(prefix="calib-")) if a.dry_run else HERE

    rows = {r["id"]: r for r in csv.DictReader((ROOT / "eval/benchmark.csv").open(encoding="utf-8-sig"))}
    results = []
    for cid in CASES:
        r = rows[cid]
        tracing.begin(cid)
        t0 = time.perf_counter()
        try:
            res, err = agent.answer(r["input"]), ""
        except Exception as e:                      # lỗi API: ghi lại, không thay bằng kết quả giả
            res, err = {"output": ""}, "%s: %s" % (type(e).__name__, e)
        s, _ = tracing.end()
        results.append({"id": cid, "type": r["type"], "input": r["input"], "expected": json.loads(r["expected"]),
                        "output": json.loads(res["output"]) if res["output"] else None, "error": err,
                        "model": ",".join(s["models"]) or "?", "tokens_in": s["tokens_in"], "tokens_out": s["tokens_out"],
                        "latency_s": round(time.perf_counter() - t0, 2)})
        print("%s · %s · token %s/%s %s" % (cid, results[-1]["model"], s["tokens_in"], s["tokens_out"], ("LỖI " + err) if err else ""))
    if any(x["error"] for x in results) and not a.dry_run:
        sys.exit("Có câu lỗi khi gọi model — KHÔNG tạo phiếu chấm. Sửa kết nối rồi chạy lại.")
    meta = {"created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "mode": "fake (dry-run)" if a.dry_run else "model thật",
            "note": "Output hiệu chỉnh cách chấm trước CP2, KHÔNG phải lượt eval chính thức.", "cases": results}
    (out_dir / "outputs.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")

    cols = ["id", "loai_cau", "tin_nhan_khach", "dap_an_dung", "output_he_thong",
            "m1_quyet_dinh_dung", "m2_an_toan_tien", "m3_trich_dan_dung", "dat_ca_cau", "ghi_chu"]
    for who in ("A", "B"):
        with (out_dir / ("cham-tay-%s.csv" % who)).open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols)
            for x in results:
                exp_keys = [k for k in FIELDS if k in x["expected"]] + ["citations"]
                exp_view = dict(x["expected"], citations=[x["expected"]["policy_id"]] + ([x["expected"]["order_id"]] if x["expected"].get("order_id") else []))
                out = x["output"]
                out_view = show(out, [k for k in FIELDS if k in exp_keys or (isinstance(out, dict) and k in out)], True) \
                    if isinstance(out, dict) else "LỖI KỸ THUẬT: " + (x["error"] or "output không phải JSON object")
                w.writerow([x["id"], x["type"], x["input"], show(exp_view, exp_keys), out_view, "", "", "", "", ""])
    print("Đã ghi outputs.json, cham-tay-A.csv, cham-tay-B.csv vào %s" % out_dir)


if __name__ == "__main__":
    main()
