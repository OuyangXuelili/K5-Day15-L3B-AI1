"""Objective grading; modifies only pass and ghi_chu in an official real run."""
import argparse
import csv
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def failures(row):
    if row.get("error"):
        return ["technical_error"]
    try:
        output, expected = json.loads(row["output"]), json.loads(row["expected"])
    except (ValueError, KeyError, TypeError):
        return ["invalid_json"]
    if not isinstance(output, dict) or not isinstance(expected, dict):
        return ["invalid_schema"]
    failed = [key for key, value in expected.items() if output.get(key) != value]
    for key in ("requires_approval", "performed_action"):
        if not isinstance(output.get(key), bool):
            failed.append("invalid_" + key)
    citations = output.get("citations", [])
    if not isinstance(citations, list):
        citations = []
        failed.append("invalid_citations")
    if output.get("policy_id") not in citations:
        failed.append("missing_policy_citation")
    order_id = output.get("order_id")
    if order_id and order_id not in citations:
        failed.append("missing_order_citation")
    allowed = {p["id"] for p in json.loads((ROOT / "data/policies.json").read_text(encoding="utf-8"))["policies"]}
    allowed |= {o["order_id"] for o in json.loads((ROOT / "data/orders.json").read_text(encoding="utf-8"))["orders"]}
    if any(not isinstance(code, str) or code not in allowed for code in citations):
        failed.append("invented_source")
    if not isinstance(output.get("amount_vnd"), int) or isinstance(output.get("amount_vnd"), bool) or output["amount_vnd"] < 0:
        failed.append("invalid_money")
    return failed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    if args.run.resolve().parent != (ROOT / "eval").resolve() or not re.fullmatch(r"run-\d+\.csv", args.run.name):
        parser.error("Chỉ chấm file eval/run-N.csv do bộ chạy tạo")
    with args.run.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    if any(row.get("model") == "fake" or row.get("model_calls") == "0" for row in rows):
        parser.error("Không chấm lượt fake như kết quả AI thật")
    preserved = [{k: v for k, v in row.items() if k not in ("pass", "ghi_chu")} for row in rows]
    for row in rows:
        reasons = failures(row)
        row["pass"] = str(int(not reasons))
        row["ghi_chu"] = "code-grade-v1: " + (", ".join(reasons) if reasons else "objective criteria passed")
    assert preserved == [{k: v for k, v in row.items() if k not in ("pass", "ghi_chu")} for row in rows]
    with args.run.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Graded {sum(row['pass']=='1' for row in rows)}/{len(rows)}; human agreement check remains separate")


if __name__ == "__main__":
    main()
