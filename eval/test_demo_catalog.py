"""Offline checks for display names and web-only item resolution."""
import copy
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
os.environ["MODEL_PROVIDER"] = "fake"
sys.path.insert(0, str(ROOT / "codebase"))
import agent
from demo_catalog import display_order, resolve_demo_item_names
from tools import normalize


class DemoCatalogTests(unittest.TestCase):
    def setUp(self):
        self.orders = json.loads((ROOT / "data/orders.json").read_text(encoding="utf-8"))["orders"]
        network = patch("urllib.request.urlopen", side_effect=AssertionError("Offline only"))
        network.start()
        self.addCleanup(network.stop)

    def test_display_names_preserve_order_values_and_source(self):
        before = copy.deepcopy(self.orders)
        for order in self.orders:
            shown = display_order(order)
            self.assertNotIn("Mẫu", shown["restaurant"])
            for item in shown["items"]:
                self.assertNotIn("mẫu", item["name"])
            restored = {**shown, "restaurant": order["restaurant"], "items": [
                {**item, "name": original["name"]}
                for item, original in zip(shown["items"], order["items"])]}
            self.assertEqual(restored, order)
            shown["items"][0]["name"] = "changed locally"
        self.assertEqual(self.orders, before)

    def test_full_display_names_resolve_to_the_selected_item(self):
        for order in self.orders[:50]:
            for item in display_order(order)["items"]:
                for name in (item["name"], normalize(item["name"]), item["name"].upper(),
                             item["name"].replace(" ", "  ")):
                    with self.subTest(order=order["order_id"], name=name):
                        text = f'{order["order_id"]} Giao thiếu 1 phần {name}.'
                        self.assertEqual(resolve_demo_item_names(text, self.orders),
                                         f'{order["order_id"]} Giao thiếu 1 phần {item["item_id"]}.')

    def test_names_do_not_cross_order_or_word_boundaries(self):
        for text in ("FD999 thiếu cơm gà xối mỡ", "thiếu cơm gà xối mỡ",
                     "FD005 FD007 thiếu cơm gà xối mỡ", "FD007 thiếu cơm gà xối mỡ",
                     "FD005 thiếu cơm gà xối mỡx"):
            with self.subTest(text=text):
                self.assertEqual(resolve_demo_item_names(text, self.orders), text)

    def test_display_names_work_through_the_existing_workflow(self):
        for name in ("Cơm thịt kho trứng", "com thit kho trung"):
            text = resolve_demo_item_names("FD007 giao thiếu 1 phần " + name, self.orders)
            result = json.loads(agent.answer(text)["output"])
            self.assertEqual(result["decision"], "draft_refund")
            self.assertEqual(result["amount_vnd"], 25000)
            self.assertEqual(result["order_id"], "FD007")
            self.assertFalse(result["performed_action"])

    def test_existing_menu_names_and_item_codes_keep_working(self):
        for text in ("FD061 Thiếu 1 phần Cơm gà", "FD061 Thiếu 1 phần I01"):
            self.assertEqual(resolve_demo_item_names(text, self.orders), text)
            result = json.loads(agent.answer(text)["output"])
            self.assertEqual(result["decision"], "draft_refund")
            self.assertEqual(result["amount_vnd"], 35000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
