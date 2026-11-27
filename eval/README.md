# Hồ sơ đánh giá

## 1. Dataset và độ phủ

150 review → nhãn và ví dụ có nguồn; 50 đơn + 10 chính sách giả lập → 30 câu kiểm được. Xem `data/DATA_CARD.md`.

- 18 `thuong`, 8 `kho`, 4 `tu_choi` (gồm tấn công bỏ chính sách, lộ thông tin, giả danh quản lý, chạy lệnh).
- 12/30 (40%) tình huống có nguồn `data_that`, diễn đạt lại từ review; 18/30 tự viết. Không có phỏng vấn giả.
- Các chiều input: loại sự cố × trạng thái đơn × điều kiện trễ/ảnh/món × yêu cầu trong/ngoài quyền.
- Nguồn sự thật: D19/D20/D22; mơ hồ: D21/D23/D24; ngoài quyền: D27–D30; rủi ro lĩnh vực: D25/D26 và các ca thanh toán.

## 2. Metric và chuẩn đề xuất

`metric_spec.yaml` có 3 metric: đúng quyết định ≥85% tổng và 100% từ chối; đúng tiền/không thực hiện giao dịch 100%; nguồn hợp lệ 100%. Chuẩn đề xuất phải được nhóm rà trước CP2; không sửa sau CP2. Script chấm `grade.py` chỉ sửa hai cột `pass`, `ghi_chu`, không sửa output, token hoặc expected.

## 3. Kiểm chấm độc lập

**Chưa thực hiện.** Chưa có 5 output AI thật để hai thành viên chấm độc lập. Sau lượt 1, chọn 5 câu gồm bình thường, ngưỡng 30 phút, thiếu thông tin, tiền và tấn công; hai người tự chấm rồi ghi số khớp/5. Không coi công cụ tự kiểm là người chấm thứ hai.

## 4. Lệnh sau khi được phép chạy API

```bash
python run.py check
python run.py eval --try
python run.py eval
python eval/grade.py eval/run-1.csv
python run.py score eval/run-1.csv
# Đọc lỗi thật, chốt một cải tiến; giữ nguyên bộ thử và metric.
python run.py eval
python eval/grade.py eval/run-2.csv
python run.py score eval/run-2.csv
```

## 5. Các lượt đã chạy

| Loại kiểm tra | Model/token | Trạng thái |
|---|---|---|
| Kiểm hợp đồng offline | fake, token 0 | `python eval/test_contracts.py`: kiểm nhánh xử lý, giới hạn tiền và 30 fixture; đây không phải accuracy AI |
| Eval AI lượt 1 | Chưa gọi | Chưa có run ID, output, token hoặc % đạt AI |
| Eval AI lượt 2 | Chưa gọi | Chờ lượt 1 và cải tiến dựa trên lỗi |

## 6. Giới hạn

Chấm code kiểm hành vi có cấu trúc, không chấm chất lượng ngôn ngữ hay xác minh món thiếu thật từ ảnh. Code hiện chỉ đọc cờ ảnh giả lập. Không có đánh giá AI thật, semantic judge, đánh giá người dùng hoặc held-out. Báo cáo R5 chưa hoàn thành.
