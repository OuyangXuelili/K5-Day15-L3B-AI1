# Canvas — AI1 · Track D1

| # | Dòng | Nội dung |
|---|---|---|
| 1 | Track + lát cắt | D1 — hỗ trợ một khiếu nại đơn giao đồ ăn bằng đề xuất có căn cứ |
| 2 | Người dùng | Khách đặt đồ ăn đang cần xử lý một đơn gặp sự cố |
| 3 | Pain | Review có phản ánh chờ hỗ trợ, chưa có bước tiếp theo hữu ích khi muốn xử lý hủy/đối soát hoặc đơn giao chậm |
| 4 | Bằng chứng | 150 review công khai; 18/150 nhắc hỗ trợ/hoàn tiền, 11/150 được gắn ngữ cảnh đồ ăn; xem evidence/data-mining.md, không suy thành tỷ lệ mọi người dùng |
| 5 | Lát cắt một câu | Một khách nhập mã đơn và một vấn đề; AI phân loại sự cố, code đối chiếu chính sách và hạn mức; khách nhận hỏi thêm, đề xuất hoặc hướng chuyển người kèm căn cứ |
| 6 | Mức tự động | Chỉ gợi ý/tạo nháp; mọi hành động tài chính chờ người duyệt, không có kết nối app thật |
| 7 | Phân công có tên | Quang: nền tảng/thiết kế/nghiệm thu/tích hợp/nộp bài; Tú: giao diện/AI/demo/video; Mạnh: bằng chứng/impact/chi phí; Ân: bộ thử/đánh giá/lỗi. Chi tiết thành viên: TEAMS.md |
| — | Cập nhật cho CP2 so với bản CP1 | Chuyển bộ thử v1 sang v2: 30 câu (11 thường, 16 khó, 3 từ chối), 11 câu có nguồn review; chốt 3 metric và chuẩn §7. Hoàn thiện sơ đồ/khung demo, data card 80 đơn; đã có 5 output model thật để hiệu chỉnh cách chấm, hai phiếu khớp 5/5. Chưa chạy eval chính thức hoặc mô phỏng chi phí; việc nộp form được xác nhận riêng trên cổng BTC. |

## Cập nhật CP4

Lượt 1 đạt 24/30 → lượt 2 đạt 30/30 trên cùng bộ đã chốt; bộ 10 câu mới đạt 9/10. Mô phỏng 100 phiên, 167 lượt hỏi, 0 lỗi, khoảng $0,00022/task thành công theo tỷ lệ lượt 2 (mức thận trọng $0,00028). Kết luận Iterate: cần đo thời gian xử lý với người thật và sửa ranh giới chính sách; chưa triển khai công khai. PDF, reflection và hồ sơ nghiệm thu được tổng hợp; việc điền/nộp checkpoint xác nhận riêng trên cổng BTC. Số đo thuộc phiên bản trước sửa demo cuối, xem `docs/final-review.md`.
