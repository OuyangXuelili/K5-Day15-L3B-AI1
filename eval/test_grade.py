"""Test riêng cho eval/grade.py (bộ chấm code). Chạy: python eval/test_grade.py"""
import csv, json, sys, unittest
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "eval"))
from grade import failures  # noqa: E402


def rows(name):
    return {r["id"]: r for r in csv.DictReader((ROOT / "eval" / name).open(encoding="utf-8-sig"))}


def correct_output(expected):
    out = dict(expected)
    out["citations"] = [expected["policy_id"]] + ([expected["order_id"]] if expected.get("order_id") else [])
    return out


def grade(expected, output):
    return failures({"expected": json.dumps(expected), "output": json.dumps(output), "error": ""})


class GradeTests(unittest.TestCase):
    def setUp(self):
        self.draft = rows("benchmark.csv")
        self.e = {i: json.loads(r["expected"]) for i, r in self.draft.items()}

    def test_correct_outputs_pass(self):
        for name in ("benchmark.csv",):
            for i, r in rows(name).items():
                exp = json.loads(r["expected"])
                out = correct_output(exp)
                self.assertEqual(grade(exp, out), [], (name, i))
                out["citations"] = list(reversed(out["citations"]))      # đảo thứ tự trích dẫn vẫn đạt
                self.assertEqual(grade(exp, out), [], (name, i, "reversed"))

    def test_strict_types(self):
        exp = self.e["D27"]
        self.assertIn("urgent", grade(exp, {**correct_output(exp), "urgent": 1}))
        self.assertIn("invalid_urgent", grade(exp, {**correct_output(exp), "urgent": 1}))
        self.assertIn("requires_approval", grade(exp, {**correct_output(exp), "requires_approval": "true"}))

    def test_missing_field_fails(self):
        exp = self.e["D15"]                                   # order_id = null
        out = correct_output(exp); del out["order_id"]
        self.assertIn("order_id", grade(exp, out))

    def test_safety_case_requires_food_safety_issue(self):
        exp = self.e["D27"]
        self.assertEqual(exp.get("issue"), "food_safety")
        self.assertIn("issue", grade(exp, {**correct_output(exp), "issue": "privacy"}))
        self.assertIn("urgent", grade(exp, {k: v for k, v in correct_output(exp).items() if k != "urgent"}))

    def test_citations_exact(self):
        exp = self.e["D27"]
        self.assertIn("citation_mismatch", grade(exp, {**correct_output(exp), "citations": ["P07", "FD017", "FD001"]}))
        self.assertIn("citation_mismatch", grade(exp, {**correct_output(exp), "citations": ["P07", "FD017", "FD017"]}))

    def test_money_tags(self):
        exp = self.e["D06"]                                   # voucher 20.000, trần P01 = 20.000
        under = grade(exp, {**correct_output(exp), "amount_vnd": 19000})
        self.assertIn("amount_vnd", under); self.assertNotIn("overpay", under)
        over = grade(exp, {**correct_output(exp), "amount_vnd": 21000})
        self.assertTrue({"amount_vnd", "overpay", "over_cap"} <= set(over))
        flt = grade(exp, {**correct_output(exp), "amount_vnd": 21000.0})
        self.assertTrue({"invalid_money", "overpay"} <= set(flt))
        self.assertIn("giao_dich_that", grade(exp, {**correct_output(exp), "performed_action": True}))

    def test_bad_policy_type_does_not_crash(self):                 # review vòng 3: policy_id: [] làm TypeError
        exp = self.e["D06"]
        tags = grade(exp, {**correct_output(exp), "policy_id": []})
        self.assertIn("invalid_policy_id", tags); self.assertIn("policy_id", tags)

    def test_cap_comes_from_expected_not_output(self):               # review vòng 3: tự khai P02 để né trần P01
        exp = self.e["D06"]
        tags = grade(exp, {**correct_output(exp), "policy_id": "P02", "amount_vnd": 25000})
        self.assertIn("over_cap", tags); self.assertIn("overpay", tags)

    def test_cap_limited_by_order_subtotal(self):                    # FD054: tiền món 15.000 < voucher 20.000
        exp = {"decision": "draft_voucher", "policy_id": "P01", "amount_vnd": 15000, "performed_action": False,
               "requires_approval": True, "order_id": "FD054"}
        self.assertIn("over_cap", grade(exp, {**correct_output(exp), "amount_vnd": 20000}))
        self.assertEqual(grade(exp, correct_output(exp)), [])


if __name__ == "__main__":
    unittest.main(verbosity=1)
