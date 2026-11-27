# Reflection — Nguyễn Công Tú

1. **Vai trò + phần mình làm:** phụ trách giao diện, kết nối AI, demo và video (`TEAMS.md`). Trước CP2, làm lại giao diện theo góc nhìn của khách. Giao diện phân biệt rõ chế độ AI thật với bản preview và báo lỗi API ra màn hình (`a25626f`, `7a303a0`, `4eb87c6`). Prompt được sửa sau khi chạy thử với model thật (`7527443`). Sau lượt 1, sửa các lỗi đã phân tích và đường xử lý an toàn trong `agent.py` và `tools.py` (`d860de9`); mô tả và giới hạn còn lại ở `docs/cai-tien-luot-2.md`. Ngoài ra quay video demo cho CP3, CP4 và chuẩn bị phần demo trong slide.

2. **AI hỗ trợ mình thế nào:** dùng Claude Code (Anthropic) cho ba việc:
   - đọc trace và kết quả chẩn đoán của lượt 1 để tìm nguyên nhân từng câu trượt;
   - đề xuất và viết bản sửa cho prompt và luật kiểm trong code;
   - viết script tự động quay video demo và dựng slide.

   Output của AI không được dùng ngay. Bản sửa đầu tiên làm một câu đang đạt bị trượt: model hiểu "đi sai địa chỉ" thành "giao sai món". Phải thêm điều kiện lời khách có từ chỉ thiếu hoặc sai món mới tính, rồi chạy lại kiểm thử. Mỗi thay đổi đều qua test offline và gọi thử model thật trước khi commit. Phần quyết định giữ lại: tiền luôn do code tính, không so khớp nguyên văn câu thử, không sửa bộ thử, đáp án hay chuẩn đã chốt. Lượt đánh giá chính thức không do AI chạy.

3. **Một câu thử trượt và điều tôi học được:** D18 "FD001 giao trễ mà còn thiếu canh nữa". Ở lượt 1, hệ thống chỉ nhận "giao chậm" và cấp voucher. Đúng ra phải hỏi khách muốn xử lý việc nào trước, vì tin nhắn có hai sự cố. Cách sửa là cho model liệt kê mọi sự cố, rồi để code quyết định hỏi lại.

   Bài học: sửa một câu trượt có thể làm hỏng câu đang đạt, nên phải chạy lại cả bộ. Bài học thứ hai: luật viết sau khi đọc câu trượt dễ khớp với cách viết của bộ thử. Vì vậy kết quả cao trên bộ đã nhìn chỉ là cận trên; muốn biết độ chính xác thật phải đo trên câu mới.
