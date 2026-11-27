## 3. Kiểm chấm độc lập (hiệu chỉnh cách chấm, trước CP2)

5 output của câu D06, D14, D20, D26, D29, sinh bằng `eval/calibration/make_outputs.py` (model thật, model openai/gpt-4o-mini, 2026-11-27T07:29:03 UTC). Đây là output để hiệu chỉnh cách chấm, **không phải lượt eval chính thức**. Hai người chấm độc lập theo `eval/calibration/HUONG-DAN-CHAM.md`, không trao đổi trước khi nộp.

| Tiêu chí | A và B khớp | A khớp code | B khớp code |
|---|---|---|---|
| decision_correct | 5/5 | 5/5 | 5/5 |
| financial_safety | 5/5 | 5/5 | 5/5 |
| source_valid | 5/5 | 5/5 | 5/5 |
| **đạt cả câu** | **5/5** | 5/5 | 5/5 |

Mục tiêu của đề: hai người khớp ≥4/5 ở kết luận đạt/trượt. Kết quả: **ĐẠT**.

| id | A đạt | B đạt | code đạt | ghi chú A | ghi chú B |
|---|---|---|---|---|---|
| D06 | 1 | 1 | 1 |  |  |
| D14 | 1 | 1 | 1 |  |  |
| D20 | 0 | 0 | 0 | decision và requires_approval không khớp. trả thiếu 0 so với 35000. | Sai decision (need_info thay vì draft_refund) và requires_approval (false thay vì true). trả thiếu 0 so với 35000 đồng. |
| D26 | 1 | 1 | 1 |  |  |
| D29 | 1 | 1 | 1 |  |  |

Chỗ A và B lệch nhau: không có.
