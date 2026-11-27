# Reflection — Trần Văn Quang

1. **Vai trò và phần việc:** Tôi là đội trưởng, phụ trách nền tảng, thiết kế workflow, tích hợp và chuẩn bị nghiệm thu/nộp bài.
   Phần việc gồm `canvas.md`, `spec.md`, nền dữ liệu 80 đơn, các ca khó riêng và giao diện local.
   Commit `da60b7f` bổ sung tên hiển thị, ảnh có nguồn và kiểm thử ánh xạ món; đợt hoàn thiện bổ sung kiểm JSON bất thường, kiểm tên món, PDF và đồng bộ hồ sơ.
   Đánh giá chính thức, chi phí, bằng chứng và demo được tổng hợp từ phần việc của các thành viên theo `TEAMS.md`.

2. **AI hỗ trợ:** Tôi dùng Codex hỗ trợ đọc yêu cầu, viết code, tạo dữ liệu giả lập, kiểm thử và soạn hồ sơ.
   Kết quả kiểm tự động được đối chiếu với các tệp run/trace đã lưu; không coi mock là kết quả AI thật.
   Khi tổng hợp slide, câu “0 lỗi tiền ở cả ba lần đo” phải sửa vì lượt 1 có hai ca trả thừa; mô phỏng cũng không có nhãn vàng để kết luận như eval.
   Các thay đổi code sau đo được ghi riêng, giữ nguyên benchmark, nhãn vàng và kết quả cũ.

3. **Một câu trượt và bài học:** D17 báo thiếu gà rán nhưng đơn không có món này; lượt 1 model gán sang Trà mẫu và hệ thống đề xuất 55.000đ.
   Tiền vẫn dưới trần nên kiểm hạn mức không đủ; cần kiểm căn cứ món trong lời khách trước khi tính tiền.
   Lượt 2 chặn được bằng code dù model vẫn nhận sai món. Đợt hoàn thiện còn chặn tên gần giống như cơm chay bị gán thành cơm gà.
   Điểm 30/30 trên bộ đã xem không bảo đảm câu mới đều đúng: held-out 9/10 và H09 còn trích sai chính sách, nên kết luận là tiếp tục cải tiến.
