# Khai báo dùng AI

AI hỗ trợ chuẩn bị sản phẩm, dữ liệu và hồ sơ. Mọi kết quả review truy được nguồn; dữ liệu giả lập ghi seed. Theo yêu cầu người dùng, chưa gọi API. Không có phỏng vấn/khảo sát/người dùng thử hoặc người chấm độc lập được ghi là đã làm.

| Việc | Công cụ AI | Nội dung hỗ trợ | Kiểm tra và giới hạn | Người phụ trách |
|---|---|---|---|---|
| Repo và thành viên | Codex | Đọc đề, chuẩn bị starter và TEAMS | Quang cung cấp tên/MSSV, xác nhận đội trưởng; kiểm máy đúng format | Quang điều phối; chưa chia phần |
| Bằng chứng | Codex | Viết script lấy 150 review, định nghĩa nhãn và đếm | Trích hai câu, bỏ tác giả; đọc ví dụ và rà regex; chưa hai người gắn nhãn độc lập | Chưa phân công |
| Dữ liệu giả lập | Codex | Sinh 50 đơn/10 chính sách | seed 20261127, cờ synthetic, không chính sách hãng thật | Chưa phân công |
| Code và giao diện | Codex | Workflow, adapter API, tiền/rủi ro, web local | Unit/HTTP/UI offline; API thật chưa thử | Chưa phân công |
| Bộ câu thử | Codex | 30 câu và tiêu chí chấm có cấu trúc | 12 diễn đạt lại từ tình huống review, 18 tự viết; không giả làm lời phỏng vấn | Chưa phân công |
| Hồ sơ và chi phí | Codex | Tổng hợp số đếm, cấu hình persona và giá | Chưa có token/accuracy/cost thật; giả định quy mô/tần suất ghi rõ tự ước tính | Chưa phân công |

Không bịa người, câu trả lời, nguồn, kết quả eval hoặc token. Không sửa output/expected/trace để khớp nhau. Thành viên phải đọc, kiểm lại và giải thích phần thực tế mình nhận trước khi ghi reflection.
