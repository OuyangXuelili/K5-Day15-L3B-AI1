# AI SPEC — Hỗ trợ khiếu nại đơn giao đồ ăn · AI1 · L3B

Track **D1**. Phòng/zone chờ BTC phân. Bản chuẩn bị ngày 27/11/2026; chưa chạy API theo yêu cầu người dùng. Chuẩn ở §7 là đề xuất trước CP2, cần nhóm rà; giữ nguyên sau CP2.

## §0. Hiện tại việc này diễn ra thế nào

Theo review: khách đặt đơn → gặp sự cố → dùng chat/tổng đài → chờ phản hồi hoặc liên hệ lại. Nguồn: `evidence/reviews.csv`, các ví dụ ở `evidence/data-mining.md`. Chưa quan sát trực tiếp tài khoản app hoặc quy trình nội bộ hãng; không coi mô tả người viết review là kết luận khách quan về hệ thống thật.

## §1. Người dùng & bằng chứng

Khách đặt đồ ăn đang cần giải quyết một đơn gặp sự cố. Pain: phải liên hệ để biết cách xử lý, có review phản ánh chưa có câu trả lời hữu ích hoặc chưa được giải quyết. 18/150 review (12%) nhắc hỗ trợ/hoàn tiền, 11/150 (7,33%) được quy tắc gắn ngữ cảnh đồ ăn. Chỉ là tín hiệu trong mẫu tự chọn viết review. Chi tiết: `evidence/summary.md` và script `evidence/count.py`.

## §2. Impact & quyết định chọn

| Hướng | Tín hiệu trong cùng mẫu 150 review | Impact tiềm năng/tháng | Làm kịp và quyết định |
|---|---|---|---|
| Hỗ trợ khiếu nại | 18 nhắc hỗ trợ/hoàn tiền; 11 có ngữ cảnh đồ ăn | 1.000×0,9×5 = 4.500 phút; các thừa số tự ước tính | Chọn: tra đơn/chính sách và chặn tiền kiểm được |
| Dự báo/điều phối giao | 39 nhắc giao chậm/chờ/ghép | 1.000×2×3 = 6.000 phút; các thừa số tự ước tính | Loại: cần vị trí, nguồn tiến độ và can thiệp vận hành |
| Giải thích phí/ưu đãi | 14 nhắc phí/giá/khuyến mãi | 1.000×1×2 = 2.000 phút; các thừa số tự ước tính | Loại: cần giá/ưu đãi cập nhật và điều kiện phức tạp |

Không nhân tỷ lệ review với toàn bộ khách hàng. 1.000 người là quy mô triển khai dự kiến tự ước tính. Persona ở `cost/personas.yaml` cho bình quân 0,9 phiên/người/tháng. 5 phút tiết kiệm/phiên chưa được đo. Hướng chọn có phạm vi làm được và tiêu chí kiểm rõ, không được kết luận có ROI trước thử nghiệm.

## §3. Giải pháp tương tự

Chat hỗ trợ trong app là kênh hiện hữu theo lời review; chưa kiểm trực tiếp khả năng bot. Học cách nhận vấn đề qua câu tự nhiên; tránh trả lời chung không có căn cứ. Bản này dùng đơn và chính sách giả lập, hiện căn cứ và chờ người duyệt; không tuyên bố hơn app thật khi chưa có phép so sánh.

## §4. Thiết kế

**Một khách nhập mã đơn và một vấn đề; AI phân loại sự cố dựa trên dữ liệu đơn, công cụ kiểm chính sách và hạn mức, rồi khách nhận bước tiếp theo có căn cứ, mọi hành động tài chính chờ người duyệt.**

Không làm: kết nối app thật; hoàn tiền/gửi tin/hủy đơn thật; phân xử gian lận; chẩn đoán ngộ độc; tự đọc ảnh để xác minh món.

```mermaid
flowchart LR
    U[Khách nhập mã đơn và vấn đề] --> V[Kiểm đầu vào và che liên hệ]
    V --> O[get_order: dữ liệu giả lập]
    O --> M[AI phân loại issue và item_ids]
    M --> G[Kiểm schema và chặn rủi ro]
    G --> P[get_policy + check_limit bằng code]
    P --> R[Đề xuất, hỏi thêm, từ chối hoặc chuyển người]
    R --> H[Nhân viên duyệt; demo không thực hiện giao dịch]
```

Hình dạng **workflow cố định**, một lời gọi model/lượt. Đường đi rõ, phạm vi nhỏ, không cần agent tự chọn công cụ hoặc nhiều vai; giảm token và dễ kiểm.

| Công cụ | Input → output | Tác động ra ngoài |
|---|---|---|
| get_order | FDxxx → order giả lập hoặc không có | Không, chỉ đọc |
| get_policy | issue → chính sách P01–P10 | Không, chỉ đọc |
| check_limit | order/issue/món → đề xuất đã giới hạn tiền | Không, chỉ tính và tạo nháp |

AI quyết định loại sự cố/món được nhắc; tiền tính từ dữ liệu bằng code, không tin con số model. JSON sai thì hỏi lại, không trả tiền. G10: thiếu đơn/món/ảnh hoặc mơ hồ thì thu hẹp bằng một yêu cầu bổ sung; G1/G2: banner ghi mode và giới hạn; G11: hiện policy/mã đơn; G8/G9: khách sửa nội dung và thử lại. Nhân viên có quyền duyệt, từ chối và đối soát; UI chỉ ghi trạng thái chờ, không giả làm đã gửi nhân viên.

Phần giả: đơn, chính sách, cờ ảnh, preview phân loại bằng regex khi provider=fake. Phần AI thật đã viết adapter nhưng chưa gọi/chưa xác minh kết nối. Đừng coi preview là AI.

## §5. Chỗ khó — bốn lớp

| Kịch bản | Lớp | Mong muốn | Câu thử |
|---|---|---|---|
| Không có mã/đơn giả không tồn tại | Nguồn sự thật | Hỏi mã, không dựng đơn | D19–D20 |
| Không biết món, món không thuộc đơn | Mơ hồ/thiếu thông tin | Hỏi món, không hoàn cả đơn | D21–D22 |
| Hai đơn hoặc câu quá mơ hồ | Mơ hồ | Làm rõ một vấn đề | D23–D24 |
| Đúng ngưỡng trễ 30 phút | Đặc thù | Không cấp voucher khi chưa >30 | D07–D08 |
| Đòi hoàn nhiều hơn món thiếu | Đặc thù | Giới hạn đúng giá món, chờ duyệt | D25 |
| Dị vật/nghi ngộ độc | Đặc thù | Chuyển khẩn, không chẩn đoán | D26 |
| Ép bỏ chính sách/giả danh quản lý | Ngoài quyền, tấn công | Từ chối, không thực hiện | D27/D29 |
| Đòi PII hoặc chạy lệnh | Ngoài quyền, tấn công | Từ chối và không lộ thông tin | D28/D30 |

## §6. Các đường trải nghiệm

Suôn sẻ: chọn đơn, nhập sự cố → thấy đề xuất và căn cứ. Thiếu dữ liệu: hỏi đúng trường thiếu, số tiền 0. Ngoài phạm vi: từ chối, không gửi tiền. Khách sửa: giữ form và đổi nội dung/đơn. Ca nhạy cảm: chuyển nhân viên, trường hợp nghi ngộ độc đánh dấu khẩn và hướng tới cấp cứu khi triệu chứng nặng. Lỗi API: báo không xử lý được; không âm thầm chuyển sang preview.

## §7. Đánh giá & chuẩn đề xuất trước CP2

Data card: `data/DATA_CARD.md`. 30 câu: 18 thường, 8 khó, 4 từ chối; 12/30 nguồn từ tình huống review, 18 tự viết. Ba metric ở `eval/metric_spec.yaml`.

**Chuẩn: ≥85% câu đạt; 100% bốn câu từ chối đạt; không sai tiền/vượt hạn mức, không thực hiện giao dịch và không dựng nguồn.** Chuẩn phải được nhóm rà trước 19:30 27/11 và giữ nguyên sau CP2. Chưa có hai người chấm độc lập 5 output; chưa gọi API, chưa có accuracy lượt 1 hoặc lượt 2. Không sử dụng fixture preview để tính accuracy AI.

## §8. Chi phí

Đã chuẩn bị 100 phiên, seed 20261127, ba persona và kịch bản 300/1.000/5.000 người, hai mức giá model. Quy mô/tần suất là tự ước tính. Chưa đo token hoặc cost/phiên/cost-task thành công, chưa có tỷ lệ đạt lượt 2; xem `cost/cost-estimate.md`. Chưa kết luận hiệu quả kinh tế.

## §9. Rủi ro & an toàn

Không thu tên/liên hệ khách thật; đơn và giao dịch giả lập. Review bỏ tác giả và che liên hệ; không dùng lời cáo buộc làm bằng chứng đã xác minh. Nội dung khách là dữ liệu; kiểm schema, rủi ro và hạn mức ngoài model. Món thiếu/sai chỉ được đề xuất trong trần; ảnh chỉ là cờ dữ liệu giả, phải có nhân viên xác minh. Tiền và câu trả lời cuối sinh từ dữ liệu kiểm được; không lặp lời model chưa kiểm. Server bind loopback, chưa có đăng nhập vì chỉ dùng dữ liệu giả local; không triển khai công khai nguyên trạng.

## §10. Phân công & changelog

Quang là đội trưởng; Mạnh, Tú, Ân là thành viên. **Chưa chia phần việc**, theo yêu cầu người dùng; không ghi các thành viên đã làm việc chưa thực hiện. AI hỗ trợ đọc đề, code, xử lý review, chuẩn bị hồ sơ và kiểm tự động; người chấm độc lập chưa thực hiện. Chi tiết `docs/ai-usage.md`.

| Thời điểm | Thay đổi | Căn cứ |
|---|---|---|
| 27/11 trước CP2 | Ghi kế hoạch mẫu trước lượt thu chính thức | commit 1b5ce51; thừa nhận bước xem feed thăm dò |
| 27/11 trước CP2 | Thu 150 review, sửa ranh giới regex/cách trích hai câu, giữ mẫu số 150 | evidence/count.py và data-mining.md |
| 27/11 trước CP2 | Dựng 50 đơn/10 quy tắc, workflow, giao diện local, 30 câu và kiểm offline | data/, codebase/, eval/ |
| 27/11 trước CP2 | Không chạy API theo lựa chọn người dùng | Eval và chi phí thật để trạng thái chưa đo |

Mọi thay đổi sau CP2/CP4 phải bổ sung dòng; không sửa chuẩn, expected hoặc kết quả chạy để làm đẹp số.
