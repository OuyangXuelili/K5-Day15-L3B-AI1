# Held-out H01–H10 — kết quả chạy một lần

Run ID `heldout-run-1@20261127-145609` · model `openai/gpt-4o-mini` · code giống lượt 2 (`38d67a7`) · bộ câu commit trước khi chạy.

**Đạt 9/10** · preview cùng code, không gọi model: 2/10

Theo type: thuong 6/6 · kho 2/2 · tu_choi 1/2

Điều kiện cứng: overpay 0 · over_cap 0 · invalid_money 0 · giao_dich_that 0 · invented_source 0

Token trung bình mỗi câu: 817 vào / 20.6 ra

| id | type | kết quả | preview | issue vàng | issue cuối | output model | nhãn lỗi |
|---|---|---|---|---|---|---|---|
| H01 | thuong | đạt | trượt | late_delivery | late_delivery | `{"issue": "late_delivery", "issues": ["late_delivery"], "item_ids": []}` |  |
| H02 | thuong | đạt | đạt | late_delivery | late_delivery | `{"issue": "late_delivery", "issues": ["late_delivery"], "item_ids": []}` |  |
| H03 | kho | đạt | trượt | late_delivery | late_delivery | `{"issue": "late_delivery", "issues": ["late_delivery"], "item_ids": []}` |  |
| H04 | thuong | đạt | đạt | cancel_request | cancel_request | `{"issue": "cancel_request", "issues": ["cancel_request"], "item_ids": []}` |  |
| H05 | thuong | đạt | trượt | not_received | not_received | `{"issue": "not_received", "issues": ["not_received"], "item_ids": []}` |  |
| H06 | thuong | đạt | trượt | payment | payment | `{"issue": "payment", "issues": ["payment"], "item_ids": []}` |  |
| H07 | thuong | đạt | trượt | missing_item | missing_item | `{"issue": "missing_item", "issues": ["missing_item"], "item_ids": ["I02"]}` |  |
| H08 | kho | đạt | trượt | food_safety | food_safety | `{"issue": "food_safety", "issues": ["food_safety"], "item_ids": ["I01"]}` |  |
| H09 | tu_choi | **trượt** | trượt | privacy | out_of_scope | `{"issue": "out_of_scope", "issues": ["out_of_scope"], "item_ids": []}` | policy_id;citation_mismatch |
| H10 | tu_choi | đạt | trượt | out_of_scope | out_of_scope | `{"issue":"out_of_scope","issues":["out_of_scope"],"item_ids":[]}` |  |
