# Giả thuyết — viết TRƯỚC khi tìm bằng chứng (5 phút, commit ngay)

> Điền ở guide bước 1.1. Ôn lại: ngày 2 · lab ngày 2.
> Viết **trước** khi đọc dòng data đầu tiên hay hỏi người đầu tiên, để không sửa cho khớp kết quả. Kết quả ngược giả thuyết vẫn đủ điểm nếu số là thật.

- Ngày giờ viết: 27/11/2026, trước lượt thu thập chính thức 150 review. Đã xem thử khả năng truy cập 50 review mỗi app và đếm từ khóa ở bước thăm dò; đây không phải giả thuyết chưa từng xem data.
- Người dùng chính: khách đặt đồ ăn qua app cần xử lý một đơn gặp sự cố.
- **Mình nghĩ:** trong mẫu review có khách chưa giải quyết được khiếu nại hoặc hoàn tiền, cần một bước tiếp theo rõ ràng dựa trên đơn và chính sách.
- **Có thể còn cách giải thích khác:** bức xúc do phí, khuyến mãi hoặc khan tài xế; một trợ lý khiếu nại không giải quyết được các nguyên nhân đó. Review Grab còn có dịch vụ gọi xe, không tự coi mọi review là giao đồ ăn.
- **Mình đúng nếu thấy:** ít nhất 5 review trong mẫu 150 có dấu hiệu hỗ trợ/khiếu nại/hoàn tiền, với ví dụ nguyên văn đủ ngữ cảnh. Đây là ngưỡng tìm tín hiệu trong mẫu review, không phải tỷ lệ của toàn bộ khách hàng.
- **Nguồn sẽ dùng:** [x] đào data · [ ] phỏng vấn ≥3 · [ ] khảo sát ≥20. Nguồn chính: review ShopeeFood App Store VN; nguồn đối chiếu: review Grab App Store VN, phân biệt dịch vụ đồ ăn/gọi xe/chưa rõ. Chưa có phỏng vấn hoặc khảo sát.

## Kế hoạch mẫu trước lượt chính thức

- Lấy 75 review mới nhất mỗi app theo feed `mostrecent`, tối đa 2 trang đầu; mọi mức sao, không lọc theo phàn nàn. Khử trùng theo ID trong từng app, giữ thứ tự feed. Nếu ít hơn thì ghi đúng số thực thu.
- Mẫu số chính là toàn bộ review được giữ, kể cả không liên quan. Báo riêng theo app và theo ngữ cảnh đồ ăn/gọi xe/chưa rõ.
- Chỉ lưu ID, ngày, số sao, link và trích tối đa hai câu đã bỏ thông tin nhận diện; không lưu tên người viết. Bản feed đầy đủ chỉ ở thư mục tạm ngoài repo.
- Đọc 30 dòng thăm dò đã ẩn danh rồi định nghĩa nhãn; ghi nhãn tự động theo quy tắc và rà ví dụ, không ghi là đã được hai người chấm độc lập.
