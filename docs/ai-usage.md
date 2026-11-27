# Khai báo dùng AI

AI hỗ trợ chuẩn bị sản phẩm, dữ liệu và hồ sơ. Mọi kết quả review truy được nguồn; dữ liệu giả lập ghi seed. Hồ sơ CP2 đã lưu 5 output hiệu chỉnh từ `openai/gpt-4o-mini` qua OpenRouter và hai phiếu chấm khớp 5/5 tại `eval/calibration/`; đây không phải lượt eval chính thức. Chưa có phỏng vấn, khảo sát hoặc người dùng thử. Lượt rà/sửa CP2 hiện tại chỉ kiểm offline, không gọi thêm API.

| Việc | Công cụ AI | Nội dung hỗ trợ | Kiểm tra và giới hạn | Người phụ trách |
|---|---|---|---|---|
| Repo và thành viên | Codex | Đọc đề, chuẩn bị starter và TEAMS | Quang cung cấp tên/MSSV, xác nhận đội trưởng; kiểm máy đúng format | Quang tiếp nhận và điều phối |
| Bằng chứng | Codex | Viết script lấy 150 review, định nghĩa nhãn và đếm | Trích hai câu, bỏ tác giả; đọc ví dụ và rà regex; chưa hai người gắn nhãn độc lập | Mạnh tiếp nhận rà soát |
| Dữ liệu giả lập | Codex | Sinh 80 đơn/10 chính sách; Quang bổ sung 30 đơn có tình huống biên | seed 20261127, cờ synthetic, giữ nguyên 50 đơn cũ; không chính sách hãng thật | Quang hoàn thiện nền, Mạnh tiếp nhận rà data card, Tú rà công cụ đọc |
| Code và giao diện | Codex | Workflow, adapter API, tiền/rủi ro, web local | Unit/HTTP/UI offline; 5 output hiệu chỉnh OpenRouter đã lưu; chưa có eval chính thức/video AI thật | Quang phụ trách nền tảng/tích hợp, Tú giao diện/demo |
| Bộ câu thử | Codex | Bộ v2: 30 câu và tiêu chí chấm có cấu trúc | 11 câu diễn đạt lại từ 11 review, 19 tự viết; nhãn vàng, metric và ngưỡng chốt CP2 | Ân phụ trách; Mạnh rà chéo |
| Tình huống khó bổ sung | Codex | 24 ca giả lập và kiểm số lượng/tiền/trạng thái thanh toán | Tập phát triển đã nhìn, chỉ kiểm fake/mock; không đổi benchmark chính hoặc khai thành accuracy AI | Quang bổ sung nền, Ân tiếp nhận đánh giá thật |
| Hồ sơ và chi phí | Codex | Tổng hợp số đếm, cấu hình persona và giá | Token hiệu chỉnh có trong outputs.json; chưa có accuracy eval chính thức hoặc cost mô phỏng; giả định ghi rõ tự ước tính | Mạnh phụ trách chi phí, Quang ghép hồ sơ |
| Phân công | Codex | Soạn trách nhiệm bốn người, trạng thái và thứ tự bàn giao | Theo yêu cầu người dùng; không coi phân công là xác nhận việc đã làm | Quang điều phối; cả nhóm rà |
| Rà soát kỹ thuật | Codex | Kiểm tra cấu trúc, 19 nhóm kiểm thử, 538 tổ hợp số lượng/chính sách, HTTP và demo desktop/mobile | Đạt ở chế độ offline; không thay cho đánh giá AI thật hoặc chấm độc lập | Quang nhận kết quả tích hợp |
| Hoàn thiện hồ sơ CP2 | Codex | Đồng bộ trạng thái, sửa bộ đếm nguồn bịa và UTF-8, thêm kiểm thử | Dựa trên bản nhóm đã push; giữ nguyên tiêu chí và hồ sơ chấm; không gọi thêm API | Quang tích hợp |

Không bịa người, câu trả lời, nguồn, kết quả eval hoặc token. Không sửa output/expected/trace để khớp nhau. Thành viên phải đọc, kiểm lại và giải thích phần thực tế mình nhận trước khi ghi reflection.
