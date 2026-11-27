# Nghiệm thu cuối — AI1

## Hồ sơ bàn giao

| Yêu cầu | Tệp/bằng chứng |
|---|---|
| Thành viên, vai trò | `TEAMS.md`, bốn tệp cá nhân trong `reflection/` |
| Người dùng, pain, so sánh hướng và thiết kế | `canvas.md`, `spec.md`, `evidence/data-mining.md` và `evidence/summary.md` |
| Demo AI ở quyết định trung tâm | `codebase/agent.py`, adapter API; output và model trong `traces/run-2.jsonl` |
| Đánh giá ≥20 câu, hai lượt và cải tiến | 30 câu chốt CP2, 24/30 → 30/30; `eval/report.md`, CSV và trace |
| Kiểm câu mới | 9/10, lỗi H09 trích P09 thay vì P08; `eval/heldout/` |
| Chi phí ≥50 phiên | 100 phiên, 167 lượt hỏi, 0 lỗi; `cost/cost-estimate.md` và `cost/simulate-1.csv` |
| Slide | `demo-slides.pdf` ở gốc; nguồn HTML có ghi chú tại `slides/demo.html` |

Video dự phòng được cung cấp riêng ở form checkpoint, không lưu đường dẫn hoặc tệp video trong repo. Điền form chưa đồng nghĩa đã nộp.

## Bản demo sau các phép đo

Ngày 27/11, sau khi giữ nguyên kết quả lượt 2 và held-out, rà mã phát hiện hai lỗi tổng quát:

- Trường `issue` hoặc phần tử `issues` là list/dict có thể gây lỗi kiểu dữ liệu, làm mất cả hướng dẫn khẩn đã nhận ra. Kiểm kiểu trước khi tra tập nhãn; JSON sai trả về hỏi thêm, dấu hiệu khẩn vẫn chuyển khẩn và không đề xuất tiền.
- Tên rút gọn có thể nhận “cơm chay” thành “Cơm gà”. Với món có tên cụ thể, phần mô tả khác không được dùng làm căn cứ trả tiền; hỏi lại mã/tên món. Tên rút gọn rõ, tên đầy đủ và mã món vẫn được giữ. Dữ liệu tên chung “mẫu” giữ hành vi cũ.

47 kiểm thử offline đạt, gồm ca sai schema, triệu chứng khẩn và tên món xung đột. Phát lại 30 phản hồi model đã lưu của lượt 2 qua code mới giữ nguyên kết luận đạt của cả 30 câu; đây là kiểm hồi quy bằng phản hồi cũ, không phải lượt AI mới. `run.py check` và kiểm dựng lại benchmark v2 cũng đạt. Không gọi API mới, không sinh hay sửa CSV/trace chính thức, không đổi prompt, dữ liệu, nhãn vàng, metric hoặc §7.

**Mốc phiên bản:** 30/30, 9/10 và mô phỏng chi phí thuộc bản đã đo trước hai sửa đổi này. Đây là bảo trì bản demo sau đánh giá; không lấy các kiểm thử offline làm số đo accuracy mới và không tuyên bố đã sửa H09. Việc thay đổi sau held-out được công bố ở đây để giữ phép đo cũ có thể kiểm lại theo commit gốc.

## Quyết định và giới hạn

**Iterate:** thử nội bộ với nhân viên duyệt mọi khoản tiền trước khi cân nhắc triển khai.

Chưa có người dùng thật, chưa đo thời gian nhân viên tiết kiệm; 5 phút cơ sở và 1 phút thận trọng đều là giả định. Khoảng 69% lượt mô phỏng còn cần nhân viên. H09 là lỗi dẫn chính sách còn mở. Đơn, quán, chính sách và cờ ảnh đều giả lập; chưa xác minh ảnh, chưa có hội thoại nhiều lượt, chặn tấn công chưa bao phủ mọi cách nói. Server chỉ dành cho local. Chi phí model chưa gồm hosting hoặc nhân viên và không phải hóa đơn thực trả.

Phần tiếp theo: kiểm với câu do người ngoài nhóm viết, đo thời gian xử lý có/không có trợ lý, thử với 2–3 người và bổ sung phiên nhiều lượt. `validation/log.md` để nguyên trạng thái chưa có buổi thử; không dựng số liệu để lấy điểm bonus.
