# Data card — AI1, Track D1

| Dataset | Nguồn | Quy mô | Vai trò |
|---|---|---:|---|
| Review công khai | App Store VN ShopeeFood 1137866760, Grab 647268330; thu 27/11/2026 | 150 đoạn, 75/app | Bằng chứng hành vi được người viết phản ánh; không dùng làm chính sách hoàn tiền |
| Đơn hàng | Nhóm dựng, `generate.py`, seed 20261127 | 80 đơn, 1–6 dòng món/đơn, 1–5 phần/dòng | `synthetic`; giữ nguyên FD001–FD050, thêm FD051–FD080; không có khách, số điện thoại, địa chỉ hoặc đơn thật |
| Chính sách | Nhóm dựng, `lab-policy-v1` | 10 quy tắc P01–P10 | `synthetic`; không đại diện chính sách của app thật |
| Bộ câu thử v2 (chốt CP2) | `eval/benchmark.csv`; nhãn vàng `eval/benchmark-gold.json`; kiểm bằng `eval/build_benchmark_v2.py --verify` | 30 câu: 11 thường, 16 khó, 3 từ chối | 11 câu diễn đạt lại tình huống từ 11 review khác nhau; 19 câu tự viết theo lời khách thật (không dấu, nói ngầm, số lượng bằng chữ, doạ, chèn lệnh). Thay bộ v1 (18/8/4) trước CP2 vì regex preview đạt 30/30 trên v1 — xem `eval/benchmark-notes.md` |
| Kiểm tra bổ sung | `eval/stress-cases.json`, tự viết theo policy giả lập | 24 tình huống khó | Dùng phát triển và kiểm tra offline; tách khỏi benchmark chính, không phải dữ liệu người dùng thật |

**Xử lý review:** lấy mẫu mostrecent, mọi mức sao, khử trùng ID, bỏ tác giả, chỉ trích tối đa hai câu nội dung, che liên hệ và định danh; gắn nhãn từ khóa trên chính đoạn đã lưu. Manifest có URL/hash nguồn. Raw cache ngoài repo. `review_id` là mã nội dung công khai, không phải mã người.

**Rà nhãn:** `missing_wrong` là nhãn từ khóa, không phải số ca thiếu/sai món đã xác minh. Hai dòng khớp gồm một dòng nói không nhận được đơn và một dòng nói về yêu cầu trả thêm phí/không giao hoặc tự hủy; không dòng nào mô tả thiếu hoặc giao sai món. Rà excerpt có mục tiêu theo nhóm từ khóa ghi nhận 0/150 tín hiệu thiếu/sai món trong lần rà này. Regex `delay` bỏ sót ít nhất hai cách nói tự nhiên (xem `evidence/data-mining.md`); chưa gắn nhãn tay độc lập toàn bộ mẫu.

**Nguồn câu thử:** `data_that: app:review_id` là tình huống được diễn đạt lại từ lời review, có thêm mã đơn và điều kiện giả lập để kiểm được. Không khẳng định nguyên văn input là do người thật hỏi, và không gọi phần bổ sung là dữ liệu thật. Phần thêm vào ngoài review được ghi trong ghi chú của từng câu ở `eval/benchmark-gold.json`, ví dụ D06 thêm chữ "giao chậm" để nêu rõ sự cố. Các câu mà review không hỗ trợ được ghi `tu_viet`.

**Quyền và riêng tư:** trích ngắn, có nguồn, không tên; không đăng raw feed. Không dùng đơn, giao dịch, tin nhắn riêng hoặc dữ liệu BTC cấp. Dữ liệu này không đại diện mọi khách hàng.

**Tái tạo:** `python data/generate.py`, `python evidence/count.py`. `python data/build_benchmark.py` dựng bộ v1 cũ, **không chạy lại** vì sẽ ghi đè bộ v2. Bộ v2: `expected` được tính từ nhãn vàng do người viết gán, đi qua `check_limit` (quy tắc P01–P10), rồi được đối chiếu tay; một reviewer độc lập tự suy lại đáp án của cả 30 câu từ `policies.json` và `orders.json`, khớp toàn bộ. `python eval/build_benchmark_v2.py --verify` so CSV và nhãn vàng với code, không ghi file. Giữ nguyên bộ đánh giá sau khi chốt; không chỉnh expected theo kết quả.

**Độ phủ bổ sung:** FD051–FD056 kiểm mốc 29/30/31 phút và voucher so với tiền món; FD057–FD064 kiểm trần hoàn đúng 100.000đ/vượt 1đ, nhiều món, nhiều phần và hoàn một phần; FD065–FD071 kiểm ảnh, đang giao, hủy, thanh toán lỗi/chưa thanh toán/chờ hoàn và bồi thường cũ; FD072–FD080 bổ sung thực đơn, món tặng 0đ, phí giao 0đ, đơn 6 dòng món và giao trễ dài. Giá 1đ hoặc lệch 1đ là fixture biên chủ động, không phải giá thị trường.

**Số lượng bị ảnh hưởng:** lấy từ cụm rõ trong câu khách như `thiếu 1 phần I01`, `giao sai 1 phần I02` hoặc tên món đầy đủ tương ứng. Không dùng số lượng/tiền do model tự trả thêm. Với dòng có nhiều phần mà thiếu số lượng, số lượng mâu thuẫn hoặc vượt số đã đặt, hỏi lại và đề xuất 0đ. Chưa hiểu mọi cách viết số lượng tự nhiên hoặc số viết bằng chữ. Cờ ảnh chỉ là dữ liệu giả lập, chưa xác minh ảnh thật.

**Chia tập:** 30 câu chính cố định dùng cho hai lượt đánh giá theo đề; 24 câu bổ sung là tập phát triển đã nhìn và dùng để sửa code. Năm câu D06, D14, D20, D26, D29 đã được chạy qua model thật trước lượt 1 để hiệu chỉnh cách chấm (`eval/calibration/`), nên không coi là chưa nhìn. Cả hai chưa phải held-out; không gộp số đạt offline thành accuracy AI. Việc thêm 30 đơn không thay dữ liệu của các đơn benchmark đã tham chiếu, policy, expected hoặc metric. Lượt eval AI thật chạy sau CP2.
