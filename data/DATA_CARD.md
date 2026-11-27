# Data card — AI1, Track D1

| Dataset | Nguồn | Quy mô | Vai trò |
|---|---|---:|---|
| Review công khai | App Store VN ShopeeFood 1137866760, Grab 647268330; thu 27/11/2026 | 150 đoạn, 75/app | Bằng chứng hành vi được người viết phản ánh; không dùng làm chính sách hoàn tiền |
| Đơn hàng | Nhóm dựng, `generate.py`, seed 20261127 | 50 đơn × 3 món | `synthetic`; không có khách, số điện thoại, địa chỉ hoặc đơn thật |
| Chính sách | Nhóm dựng, `lab-policy-v1` | 10 quy tắc P01–P10 | `synthetic`; không đại diện chính sách của app thật |
| Bộ câu thử | `build_benchmark.py` trước các lượt chạy | 30 câu: 18 thường, 8 khó, 4 từ chối | 12 câu diễn đạt lại tình huống từ review; 18 câu tự viết theo chính sách/an toàn |

**Xử lý review:** lấy mẫu mostrecent, mọi mức sao, khử trùng ID, bỏ tác giả, chỉ trích tối đa hai câu nội dung, che liên hệ và định danh; gắn nhãn từ khóa trên chính đoạn đã lưu. Manifest có URL/hash nguồn. Raw cache ngoài repo. `review_id` là mã nội dung công khai, không phải mã người.

**Nguồn câu thử:** `data_that: app:review_id` là tình huống được diễn đạt lại từ lời review, có thêm mã đơn và điều kiện giả lập để kiểm được. Không khẳng định nguyên văn input là do người thật hỏi, và không gọi phần bổ sung là dữ liệu thật. Ví dụ thiếu ảnh được ghi `tu_viet`, vì review nguồn chỉ nói đã gửi bằng chứng.

**Quyền và riêng tư:** trích ngắn, có nguồn, không tên; không đăng raw feed. Không dùng đơn, giao dịch, tin nhắn riêng hoặc dữ liệu BTC cấp. Dữ liệu này không đại diện mọi khách hàng.

**Tái tạo:** `python data/generate.py`, `python evidence/count.py`. `python data/build_benchmark.py` chỉ để dựng trước lượt thật; script từ chối chạy khi có `run-N.csv`. Giữ nguyên bộ đánh giá sau khi chốt; không chỉnh expected theo kết quả.

**Chia tập:** bộ nhỏ cố định dùng cho hai lượt đánh giá theo đề; chưa có held-out. Bộ thử đã được dùng để kiểm hợp đồng offline, nên không gọi đây là tập chưa nhìn. Chưa chạy AI thật theo yêu cầu người dùng.
