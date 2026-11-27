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

## Đối chiếu bốn checkpoint

Rà bản `6b148a0` và các tệp bàn giao ngày 28/11/2026 (GMT+7), theo [checklist BTC](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/02-guide.md) và [rubric](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/03-rubric.md).

| Mốc và hạn | Hồ sơ đã kiểm | Trạng thái |
|---|---|---|
| CP1 — 17:00 27/11 | Repo public đúng tên, TEAMS bốn người/đội trưởng dòng 1, Track D, pain/lát cắt, Canvas bảy dòng | Đủ tệp trong repo; cần đối chiếu biên nhận để biết đã nộp đúng hạn |
| CP2 — 19:30 27/11 | Canvas ghi thay đổi, bằng chứng/cách đếm, sơ đồ §4, 30 câu thử, ba metric, data card, preview; chuẩn §7 chốt ở `e807241` lúc 14:48 GMT+7 ngày 27/11 | Đủ tệp; không đổi chuẩn sau CP2. Việc nộp form là bước riêng |
| CP3 — 10:00 28/11 | 150 review và sáu trích dẫn, 30 câu (16 khó, ba từ chối), AI thật, video 30 giây cung cấp riêng, lượt 1 có run ID/token và 24/30, spec §0–§7 | Đủ hồ sơ để nộp; không coi bản nháp form là biên nhận |
| CP4 — 14:30 28/11 | Lượt 2 đạt 30/30, phân tích lỗi/cải tiến, hồ sơ đánh giá, mô phỏng 100 phiên, hai mức model/ba kịch bản, spec §0–§9, PDF tám trang ở gốc, video dự phòng 1:53 cung cấp riêng | Đủ bốn điều kiện cứng và tệp bắt buộc; kiểm phòng/zone và biên nhận trên cổng BTC; gửi nếu chưa nộp |

Đủ tệp ở bản cuối không chứng minh đã nộp checkpoint đúng giờ. Không tự xác nhận điểm hoặc việc tham gia buổi demo từ trạng thái Git.

## Rà lại cách chạy và phép tính

- Sửa `docs/connect-model.md` và `.env.example` theo adapter đã cài: `fake`, `openai`, `openrouter`; bỏ chỉ dẫn chép code mẫu và cấu hình nhà cung cấp chưa hỗ trợ. Không đổi adapter hoặc prompt.
- Bổ sung bộ 10 câu mới vào data card; đồng bộ khả năng đọc số viết bằng chữ và ghi rõ baseline 28/30 thuộc code trước cải tiến lượt 2. Giữ nguyên nội dung §7.
- Tính lại từ CSV: lượt 1 24/30, lượt 2 30/30, held-out 9/10, token mô phỏng 134.746 vào/3.597 ra. Chi phí mẫu trung bình $0,00022370/phiên; chi phí tháng cơ sở theo từng persona $0,28795. Đã giải thích khác biệt cơ cấu phiên trong `cost/cost-estimate.md`, không sửa CSV/tóm tắt mô phỏng gốc.
- Kiểm lại demo local bằng OpenAI trực tiếp `gpt-4o-mini-2024-07-18`: giao chậm → voucher 20.000đ; thiếu một trong ba phần → 35.000đ; chèn lệnh → từ chối, 0đ. Cả ba có một lời gọi model, token từ API và `performed_action=false`. Đây là kiểm kết nối/hành vi demo, không phải lượt eval hay tỷ lệ đạt mới; các số đo chính thức vẫn dùng OpenRouter.
- `run.py check`, kiểm benchmark v2 và 47 kiểm thử offline đều đạt. Tệp kết quả/trace, evidence, dữ liệu, metric và bộ chạy BTC được giữ nguyên.

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

Phần con người còn làm trước hạn: đội trưởng nộp form đúng mốc; kiểm phòng/zone trên cổng BTC; mỗi thành viên đọc reflection, nắm phần mình và trình bày ít nhất một phần khi demo. Sau buổi demo, nếu có góp ý thì cập nhật changelog §10 trước 23:59 ngày 28/11. Nguồn phỏng vấn/khảo sát đối chiếu riêng (R1) và người dùng thử ngoài nhóm (bonus) chưa có; các phần này cần thu thật, không thể thay bằng dữ liệu giả hoặc AI đóng vai.
