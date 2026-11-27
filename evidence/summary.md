# Bằng chứng và quyết định

**Người dùng:** khách đặt đồ ăn đang cần xử lý một đơn có sự cố.

**Pain được quan sát:** trong review có khách mô tả việc chờ hỗ trợ, không nhận được phản hồi, cần xử lý hủy/đối soát nhưng chưa biết bước tiếp theo. Đây là phản ánh của người viết, không phải kết luận kiểm toán dịch vụ.

- Mẫu: 150 review công khai, 75 mỗi app, mọi mức sao.
- 18/150 (12,00%) nhắc hỗ trợ/hoàn tiền; trong đó 11/150 (7,33%) được quy tắc gắn ngữ cảnh đồ ăn.
- Bộ đếm từ khóa đánh dấu 2/150 dòng `missing_wrong`; rà nguồn cho thấy một dòng nói không nhận được đơn, dòng còn lại nói về yêu cầu trả thêm phí/không giao hoặc tự hủy. Không dòng nào mô tả thiếu hoặc giao sai món (**0/150 trong lần rà có mục tiêu**); không dùng nhãn máy này làm bằng chứng cho pain thiếu/sai món.
- Bộ đếm `delay` cho 39/150; regex đã bỏ sót ví dụ “Giao hàng thì lâu” và “lúc nào cũng ghép”. 39 là số máy đếm theo quy tắc hiện tại, chưa phải số đầy đủ sau gắn nhãn tay.
- Nguồn, sáu trích dẫn và cách đếm: [data-mining.md](data-mining.md); số máy đọc: [counts.json](counts.json).
- Mẫu và nhãn từng dòng: [reviews-labeled.csv](reviews-labeled.csv). Không có người trong nhóm, người phỏng vấn giả hoặc lời AI đóng vai khách.

**Kết luận:** có tín hiệu đủ để làm bản chạy thử hỗ trợ khiếu nại. Chưa chứng minh trợ lý sẽ giảm bao nhiêu phút, tăng hài lòng hoặc giảm khiếu nại. Không dùng dữ liệu này để xếp hạng hãng, tài xế hoặc khách.

**Lát cắt chọn:** một khách nhập mã đơn và một vấn đề; hệ thống tra dữ liệu giả lập, phân loại sự cố, kiểm chính sách bằng code và trả bước tiếp theo có căn cứ. Chỉ tạo bản nháp chờ người duyệt.

**Hướng bị loại:** dự báo/điều phối giao hàng cần dữ liệu vị trí và khả năng can thiệp vận hành; tối ưu phí/khuyến mãi cần bảng giá động. Bản thử khiếu nại có phạm vi và điều kiện chấm rõ hơn trong thời gian hackathon.

**Nguồn đối chiếu:** hai tập review hai app được lấy bằng cùng phương pháp; chưa có nguồn phỏng vấn/khảo sát độc lập. Việc kiểm hai dòng `missing_wrong` là rà soát có mục tiêu, không thay thế gắn nhãn tay độc lập toàn bộ mẫu.
