# Báo cáo đánh giá — trạng thái chuẩn bị

Theo yêu cầu của người dùng: **chưa gọi API**. Chưa có lượt 1/lượt 2, accuracy AI, số token hoặc chi phí đo. Không thay các phần này bằng kết quả preview.

| Lượt | Run ID | Model | Đạt/tổng | Trạng thái |
|---|---|---|---|---|
| 1 | Chưa có | Chưa gọi | Chưa đo | Chờ cho phép chạy API |
| 2 | Chưa có | Chưa gọi | Chưa đo | Chờ đọc lỗi lượt 1 và một cải tiến |

## Việc phải bổ sung bằng kết quả thật

1. Lưu `run-1.csv`, chấm theo metric, giữ nguyên output/token/trace.
2. Phân tích ít nhất 3 lỗi thật: input, output, nguyên nhân và nhóm lỗi. Nếu chưa quan sát được đủ lỗi thì ghi thiếu, không tạo lỗi giả hoặc cố ý làm hỏng baseline.
3. Chọn một nhóm lỗi quan trọng, cải tiến code/prompt, chạy cùng 30 câu thành `run-2.csv`, báo cả regression.
4. Hai người chấm độc lập 5 output, ghi độ khớp trong `eval/README.md`.

## Lỗi kỹ thuật đã tìm và sửa khi chuẩn bị

- Regex preview từng khớp `huye` bên trong `chuyen`, khiến câu mơ hồ bị phân loại hủy đơn; đã bổ sung ranh giới từ. Đây là lỗi preview offline, không nhận là lỗi eval AI.
- Script thu review ban đầu ghi file thành công nhưng in đường dẫn Unicode lỗi trên console Windows; đã đặt output UTF-8. Không mất hoặc thay số đo.
- Regex sàng lọc review ban đầu khớp chuỗi con; đã sửa ranh giới trước khi chốt bản số liệu hiện tại.
- Dòng món có nhiều phần từng được tính hoàn cả dòng dù chưa rõ số lượng thiếu. Đã tách số lượng bị ảnh hưởng từ câu khách; thiếu/mâu thuẫn/vượt số đã đặt thì hỏi lại, số tiền 0. Kiểm offline gồm hoàn 1 trong 3 phần và các tổ hợp số lượng hợp lệ.
- Ánh xạ tên món preview từng cố định cơm/canh/trà theo I01/I02/I03; đã tra thực đơn của đúng đơn và tránh lấy chữ `tra` trong `kiểm tra` làm món bị thiếu. Prompt AI cũng tra ID theo từng đơn; chưa đo bằng model thật.
- Đơn có trạng thái thanh toán khác `paid` được chuyển đối soát thay vì tạo nháp bồi thường. Thêm guard cho lệnh bỏ hướng dẫn bằng tiếng Anh và nhiều yêu cầu trong preview. Đây là cải tiến trước eval thật, không ghi là kết quả lượt 1→2.
