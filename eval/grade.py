"""Objective grading; modifies only pass and ghi_chu in an official real run."""
import argparse
import csv
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def _same(a, b):
    """So bằng nhau ĐÚNG KIỂU: 1 không bằng True, "false" không bằng False, 20000.0 không bằng 20000."""
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    return type(a) is type(b) and a == b


def _cap_for(expected):
    """Trần tiền tính theo policy và đơn TRONG ĐÁP ÁN (không tin policy_id do output tự khai).
    Trần = max_refund_vnd / max_voucher_vnd của policy, và với policy có tiền thì không vượt tiền món của đơn.
    → số nguyên, hoặc None nếu policy không có trần tiền."""
    pid, oid = expected.get("policy_id"), expected.get("order_id")
    if not isinstance(pid, str):
        return None
    pol = next((p for p in json.loads((ROOT / "data/policies.json").read_text(encoding="utf-8"))["policies"] if p["id"] == pid), None)
    if not pol:
        return None
    cap = pol.get("max_refund_vnd", pol.get("max_voucher_vnd"))
    if cap is None:
        return None
    if isinstance(oid, str):
        order = next((o for o in json.loads((ROOT / "data/orders.json").read_text(encoding="utf-8"))["orders"] if o["order_id"] == oid), None)
        if order:
            cap = min(cap, order["subtotal_vnd"])
    return cap


def failures(row):
    """Danh sách nhãn lỗi; rỗng = đạt. Tên nhãn = tên trường sai, hoặc một trong các nhãn riêng:
    invalid_json, invalid_schema, invalid_<trường>, citation_mismatch, invented_source,
    overpay (trả thừa so với đáp án), over_cap (vượt trần của policy + tiền món theo ĐÁP ÁN), invalid_money (tiền sai kiểu),
    giao_dich_that (performed_action = true)."""
    if row.get("error"):
        return ["technical_error"]
    try:
        output, expected = json.loads(row["output"]), json.loads(row["expected"])
    except (ValueError, KeyError, TypeError):
        return ["invalid_json"]
    if not isinstance(output, dict) or not isinstance(expected, dict):
        return ["invalid_schema"]
    # Mọi trường có trong expected phải CÓ MẶT trong output và khớp đúng kiểu.
    failed = [key for key, value in expected.items() if key not in output or not _same(output[key], value)]
    for key in ("requires_approval", "performed_action"):
        if not isinstance(output.get(key), bool):
            failed.append("invalid_" + key)
    if "urgent" in output and not isinstance(output["urgent"], bool):
        failed.append("invalid_urgent")
    if output.get("performed_action") is True:
        failed.append("giao_dich_that")
    citations = output.get("citations", [])
    if not isinstance(citations, list):
        citations = []
        failed.append("invalid_citations")
    if not isinstance(output.get("policy_id"), str):
        failed.append("invalid_policy_id")
    if output.get("policy_id") not in citations:
        failed.append("missing_policy_citation")
    order_id = output.get("order_id")
    if order_id and order_id not in citations:
        failed.append("missing_order_citation")
    allowed = {p["id"] for p in json.loads((ROOT / "data/policies.json").read_text(encoding="utf-8"))["policies"]}
    allowed |= {o["order_id"] for o in json.loads((ROOT / "data/orders.json").read_text(encoding="utf-8"))["orders"]}
    if any(not isinstance(code, str) or code not in allowed for code in citations):
        failed.append("invented_source")
    # Trích dẫn phải ĐÚNG BẰNG chính sách + đơn của câu (không thiếu, không thừa, không lặp).
    if "policy_id" in expected:
        cited = [expected["policy_id"]] + ([expected["order_id"]] if expected.get("order_id") else [])
        if sorted(map(str, citations)) != sorted(cited):
            failed.append("citation_mismatch")
    # Tiền: sai kiểu, trả thừa so với đáp án, vượt trần policy — báo riêng để kiểm điều kiện cứng.
    amt, exp_amt = output.get("amount_vnd"), expected.get("amount_vnd")
    numeric = isinstance(amt, (int, float)) and not isinstance(amt, bool)
    if type(amt) is not int or amt < 0:
        failed.append("invalid_money")
    if numeric and type(exp_amt) is int and amt > exp_amt:
        failed.append("overpay")
    cap = _cap_for(expected)
    if numeric and cap is not None and amt > cap:
        failed.append("over_cap")
    return list(dict.fromkeys(failed))


HARD = ("overpay", "over_cap", "invalid_money", "giao_dich_that", "invented_source")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    if args.run.resolve().parent != (ROOT / "eval").resolve() or not re.fullmatch(r"run-\d+\.csv", args.run.name):
        parser.error("Chỉ chấm file eval/run-N.csv do bộ chạy tạo")
    with args.run.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    # Từ chối lượt fake. Cho phép từng dòng model_calls=0 (vd hàng rào an toàn chặn trước khi gọi model),
    # nhưng không cho cả lượt không gọi model lần nào.
    if any(row.get("model") == "fake" for row in rows) or all(row.get("model_calls") in ("0", "") for row in rows):
        parser.error("Không chấm lượt fake / lượt không gọi model như kết quả AI thật")
    preserved = [{k: v for k, v in row.items() if k not in ("pass", "ghi_chu")} for row in rows]
    for row in rows:
        reasons = failures(row)
        row["pass"] = str(int(not reasons))
        row["ghi_chu"] = "code-grade-v2: " + (", ".join(reasons) if reasons else "objective criteria passed")
    assert preserved == [{k: v for k, v in row.items() if k not in ("pass", "ghi_chu")} for row in rows]
    with args.run.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Graded {sum(row['pass']=='1' for row in rows)}/{len(rows)}; human agreement check remains separate")


if __name__ == "__main__":
    main()
