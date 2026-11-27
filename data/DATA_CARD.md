# Data card — AI1, Track D1

| Dataset | Nguồn | Quy mô | Vai trò |
|---|---|---:|---|
| Review công khai | App Store VN ShopeeFood 1137866760, Grab 647268330; thu 27/11/2026 | 150 đoạn, 75/app | Bằng chứng hành vi được người viết phản ánh; không dùng làm chính sách hoàn tiền |
| Đơn hàng | Nhóm dựng, `generate.py`, seed 20261127 | 80 đơn, 1–6 dòng món/đơn, 1–5 phần/dòng | `synthetic`; giữ nguyên FD001–FD050, thêm FD051–FD080; không có khách, số điện thoại, địa chỉ hoặc đơn thật |
| Chính sách | Nhóm dựng, `lab-policy-v1` | 10 quy tắc P01–P10 | `synthetic`; không đại diện chính sách của app thật |
| Bộ câu thử | `build_benchmark.py` trước các lượt chạy | 30 câu: 18 thường, 8 khó, 4 từ chối | 12 câu diễn đạt lại tình huống từ review; 18 câu tự viết theo chính sách/an toàn |
| Kiểm tra bổ sung | `eval/stress-cases.json`, tự viết theo policy giả lập | 24 tình huống khó | Dùng phát triển và kiểm tra offline; tách khỏi benchmark chính, không phải dữ liệu người dùng thật |

**Xử lý review:** lấy mẫu mostrecent, mọi mức sao, khử trùng ID, bỏ tác giả, chỉ trích tối đa hai câu nội dung, che liên hệ và định danh; gắn nhãn từ khóa trên chính đoạn đã lưu. Manifest có URL/hash nguồn. Raw cache ngoài repo. `review_id` là mã nội dung công khai, không phải mã người.

**Nguồn câu thử:** `data_that: app:review_id` là tình huống được diễn đạt lại từ lời review, có thêm mã đơn và điều kiện giả lập để kiểm được. Không khẳng định nguyên văn input là do người thật hỏi, và không gọi phần bổ sung là dữ liệu thật. Ví dụ thiếu ảnh được ghi `tu_viet`, vì review nguồn chỉ nói đã gửi bằng chứng.

**Quyền và riêng tư:** trích ngắn, có nguồn, không tên; không đăng raw feed. Không dùng đơn, giao dịch, tin nhắn riêng hoặc dữ liệu BTC cấp. Dữ liệu này không đại diện mọi khách hàng.

**Tái tạo:** `python data/generate.py`, `python evidence/count.py`. `python data/build_benchmark.py` chỉ để dựng trước lượt thật; script từ chối chạy khi có `run-N.csv`. Giữ nguyên bộ đánh giá sau khi chốt; không chỉnh expected theo kết quả.

**Độ phủ bổ sung:** FD051–FD056 kiểm mốc 29/30/31 phút và voucher so với tiền món; FD057–FD064 kiểm trần hoàn đúng 100.000đ/vượt 1đ, nhiều món, nhiều phần và hoàn một phần; FD065–FD071 kiểm ảnh, đang giao, hủy, thanh toán lỗi/chưa thanh toán/chờ hoàn và bồi thường cũ; FD072–FD080 bổ sung thực đơn, món tặng 0đ, phí giao 0đ, đơn 6 dòng món và giao trễ dài. Giá 1đ hoặc lệch 1đ là fixture biên chủ động, không phải giá thị trường.

**Số lượng bị ảnh hưởng:** lấy từ cụm rõ trong câu khách như `thiếu 1 phần I01`, `giao sai 1 phần I02` hoặc tên món đầy đủ tương ứng. Không dùng số lượng/tiền do model tự trả thêm. Với dòng có nhiều phần mà thiếu số lượng, số lượng mâu thuẫn hoặc vượt số đã đặt, hỏi lại và đề xuất 0đ. Chưa hiểu mọi cách viết số lượng tự nhiên hoặc số viết bằng chữ. Cờ ảnh chỉ là dữ liệu giả lập, chưa xác minh ảnh thật.

**Chia tập:** 30 câu chính cố định dùng cho hai lượt đánh giá theo đề; 24 câu bổ sung là tập phát triển đã nhìn và dùng để sửa code. Cả hai chưa phải held-out; không gộp số đạt offline thành accuracy AI. Việc thêm 30 đơn không thay dữ liệu của các đơn benchmark đã tham chiếu, policy, expected hoặc metric. Chưa chạy AI thật theo yêu cầu người dùng.
