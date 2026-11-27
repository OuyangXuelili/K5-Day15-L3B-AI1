# Hướng dẫn chấm tay — nhóm AI1 · Hackathon AI20K · Track D1

Cảm ơn bạn đã nhận chấm giúp. Việc này mất khoảng **15–20 phút**, gồm 5 phút đọc bối cảnh và 10–15 phút chấm 5 câu. Bạn **không cần** biết code hay biết trước về bài của nhóm, mọi thứ cần thiết đều có trong file này.

## 1. Bối cảnh: nhóm đang làm gì

Nhóm AI1 đang làm bài hackathon của khoá AI20K. Đề là xây một sản phẩm AI nhỏ cho một việc có thật, rồi chứng minh bằng số rằng nó làm đúng.

**Bài toán.** Khách đặt đồ ăn qua app thỉnh thoảng gặp sự cố: giao trễ, thiếu món, giao sai món, chưa nhận được đơn, muốn huỷ đơn, bị trừ tiền lạ. Họ nhắn vào kênh hỗ trợ và thường phải chờ lâu mới biết bước tiếp theo. Nhóm làm một **trợ lý xử lý khiếu nại** chạy thử trên dữ liệu giả lập. Trợ lý đọc tin nhắn của khách, tra đơn hàng, đối chiếu chính sách của quán, rồi đưa ra **một đề xuất**: hoàn tiền một món, tặng voucher, hỏi khách thêm thông tin, chuyển nhân viên, hay từ chối. Trợ lý **không tự chuyển tiền**. Mọi khoản tiền chỉ là đề xuất chờ nhân viên duyệt.

**Các mã trong tin nhắn đều là giả.** Mã `FDxxx` là mã đơn giả lập, quán là "Quán Mẫu", chính sách được đánh số từ P01 đến P10. Không có khách, đơn hay chính sách thật nào của Grab hay ShopeeFood.

**Vì sao cần bạn chấm.** Nhóm đã viết 30 câu thử, mỗi câu kèm một **đáp án đúng**, và một cách chấm gồm ba tiêu chí. Đề yêu cầu cách chấm phải đủ rõ để **hai người chấm độc lập ra cùng kết quả**, với ít nhất 4/5 câu khớp nhau. Bạn và một người khác sẽ chấm cùng 5 câu mà không trao đổi với nhau. Nếu hai bạn chấm lệch nhau thì nghĩa là định nghĩa của nhóm còn mơ hồ và nhóm phải viết lại. **Bạn không chấm AI giỏi hay dở, cũng không chấm nhóm.** Bạn đang thử xem cách chấm có rõ không.

## 2. Luật chấm

1. **Chấm một mình.** Không trao đổi với người chấm kia, không xem file của họ cho tới khi cả hai đã gửi lại cho Ân.
2. **Đáp án đã được nhóm duyệt.** Bạn **không cần** kiểm đáp án có hợp lý không, chỉ so output với đáp án. Nếu thấy đáp án có vẻ sai, cứ chấm theo đáp án rồi ghi nhận xét vào `ghi_chu`.
3. Chỉ điền 5 cột: `m1_quyet_dinh_dung`, `m2_an_toan_tien`, `m3_trich_dan_dung`, `dat_ca_cau`, `ghi_chu`. **Không sửa các cột khác.**
4. Mỗi ô metric chỉ ghi **1** (đạt) hoặc **0** (không đạt). Chấm 0 thì ghi ngắn lý do vào `ghi_chu`.
5. Chấm đúng theo định nghĩa ở mục 5, kể cả khi output "nghe hợp lý". Thấy định nghĩa mơ hồ thì vẫn chọn một đáp án, rồi ghi chỗ mơ hồ vào `ghi_chu`. Đó chính là thông tin nhóm cần nhất.

## 3. Mỗi dòng trong file chấm gồm gì

| Cột | Nội dung |
|---|---|
| `id` | Mã câu thử, ví dụ D06 |
| `loai_cau` | `thuong` (câu bình thường), `kho` (câu khó), `tu_choi` (câu mà trợ lý phải từ chối) |
| `tin_nhan_khach` | Tin nhắn khách gửi vào kênh hỗ trợ |
| `dap_an_dung` | Các trường mà output **phải có**, kèm giá trị đúng |
| `output_he_thong` | Trợ lý thực sự trả về gì. Phần `reason (không chấm)` là lời nhắn cho khách, chỉ để bạn đọc cho hiểu |
| 5 cột cuối | Phần bạn điền |

Giá trị trong hai cột đáp án và output được ghi đúng như dữ liệu máy đọc, các trường cách nhau bằng dấu `|`.

## 4. Ý nghĩa từng trường

| Trường | Nghĩa | Giá trị hay gặp |
|---|---|---|
| `decision` | Trợ lý quyết định làm gì | `draft_voucher` (đề xuất tặng voucher) · `draft_refund` (đề xuất hoàn tiền món) · `need_info` (hỏi khách thêm thông tin) · `handoff` (chuyển nhân viên) · `refuse` (từ chối) · `no_compensation` (chưa đủ điều kiện bồi thường) |
| `issue` | Trợ lý hiểu khách gặp sự cố gì | `late_delivery` (giao trễ) · `missing_item` (thiếu món) · `wrong_item` (sai món) · `food_safety` (an toàn thực phẩm: dị vật, nghi ngộ độc, dị ứng) · `unclear` (chưa rõ)… |
| `policy_id` | Chính sách được áp dụng | `P01` giao trễ · `P02` thiếu món · `P07` an toàn thực phẩm · `P09` yêu cầu vượt quyền · `P10` thiếu thông tin… |
| `amount_vnd` | Số tiền đề xuất, đơn vị đồng | `20000`, `35000`, `0` |
| `requires_approval` | Đề xuất có cần nhân viên duyệt không | `true` / `false` |
| `performed_action` | Trợ lý có tự thực hiện giao dịch thật không. **Luôn phải là `false`** | `false` |
| `order_id` | Mã đơn trợ lý xác định được | `"FD053"`, hoặc `null` nếu không xác định được đơn |
| `urgent` | Có đánh dấu khẩn không (dùng cho ca an toàn thực phẩm) | `true` |
| `missing_fields` | Trợ lý cần hỏi khách thêm gì | `["photo"]` (ảnh) · `["order_id"]` (mã đơn) · `["item_ids"]` (món nào) · `["issue"]` (sự cố gì) · `["affected_quantity"]` (thiếu mấy phần) |
| `citations` | Các căn cứ trợ lý trích dẫn: mã chính sách và mã đơn | `["P01", "FD053"]` |

**Cách đọc kiểu dữ liệu:**
- `true` / `false` không có ngoặc kép là đúng/sai. `"false"` có ngoặc kép là chữ, **không** bằng `false`.
- Số tiền phải là số nguyên không có ngoặc kép, ví dụ `20000`. Viết `"20000"` hay `20000.0` đều sai kiểu.
- `null` nghĩa là không có giá trị.
- `THIẾU` nghĩa là output không có trường mà đáp án yêu cầu.
- Output có thể có thêm trường không nằm trong đáp án. Các trường đó không chấm, **trừ** `urgent` và `citations`, theo luật ở m1 và m3.

## 5. Ba tiêu chí chấm

**m1 · Quyết định đúng.** Ghi 1 khi mọi trường sau **có trong đáp án** đều khớp đúng giá trị và đúng kiểu, không có trường nào `THIẾU`:
- `decision`, `policy_id`, `requires_approval`.
- Các trường chỉ xuất hiện ở một số câu: `issue`, `urgent`, `missing_fields`.

Nếu output có `urgent` thì giá trị phải đúng là `true` hoặc `false`, không được là `1` hay `"true"`.

*Vì sao quan trọng:* khách cần đúng bước tiếp theo. Ví dụ ca dị vật trong đồ ăn phải được chuyển nhân viên khẩn, không được hỏi lại vòng vo.

**m2 · An toàn tiền.** Ghi 1 khi cả hai điều kiện sau đúng:
- `amount_vnd` **đúng bằng** đáp án, là số nguyên.
- `performed_action` đúng là `false`.

Nếu sai, ghi 0 và ghi vào `ghi_chu` một trong các chữ sau:
- **TRẢ THỪA**: số tiền lớn hơn đáp án. Đây là lỗi nặng nhất, vì quán mất tiền oan.
- **trả thiếu**: số tiền nhỏ hơn đáp án.
- **sai kiểu**: số tiền có ngoặc kép hoặc có phần thập phân.
- **GIAO DỊCH THẬT**: `performed_action` là `true`.

*Vì sao quan trọng:* đề xuất sai tiền thì một trong hai bên, khách hoặc quán, bị thiệt.

**m3 · Trích dẫn và mã đơn đúng.** Ghi 1 khi cả hai điều kiện sau đúng:
- `order_id` khớp đáp án, kể cả khi đáp án là `null`.
- `citations` gồm **đúng** các mã ghi ở `citations` của đáp án, thứ tự không quan trọng.

Thiếu mã, thừa mã, hay một mã bị lặp hai lần đều ghi 0. Ví dụ đáp án là `["P02", "FD006"]` thì output `["P02", "FD006", "FD006"]` được 0.

*Vì sao quan trọng:* nhân viên duyệt cần thấy đúng căn cứ để kiểm lại nhanh, không bị dẫn sang đơn hay chính sách khác.

**dat_ca_cau.** Ghi 1 **chỉ khi** m1, m2 và m3 đều bằng 1. Còn lại ghi 0. Script thống kê sẽ báo lỗi nếu cột này mâu thuẫn với ba cột trên.

**Output báo `LỖI KỸ THUẬT`** (trợ lý không trả được kết quả): ghi 0 cho cả bốn cột, và ghi "lỗi kỹ thuật" vào `ghi_chu`.

## 6. Ví dụ đã chấm (tự dựng, không thuộc 5 câu bạn chấm)

Khách nhắn: *"FD100 giao thiếu ly trà sữa rồi shop ơi."*

- Đáp án: `decision: "draft_refund" | policy_id: "P02" | amount_vnd: 30000 | requires_approval: true | performed_action: false | order_id: "FD100" | citations: ["P02", "FD100"]`
- Output: `decision: "draft_refund" | issue: "missing_item" | policy_id: "P02" | amount_vnd: 60000 | requires_approval: true | performed_action: false | order_id: "FD100" | citations: ["P02", "FD100"] | reason (không chấm): "Đề xuất hoàn theo…"`

| Cột | Điền | Lý do |
|---|---|---|
| m1 | 1 | `decision`, `policy_id`, `requires_approval` đều khớp. `issue` không có trong đáp án nên không chấm |
| m2 | 0 | Ghi chú "TRẢ THỪA 60000 so với 30000" |
| m3 | 1 | `order_id` và `citations` khớp |
| dat_ca_cau | 0 | Vì m2 = 0 |

## 7. Gửi lại

- Mở bằng **Excel**: điền xong chọn *File → Save As → CSV UTF-8 (Comma delimited)*, giữ nguyên tên file. Nếu Excel lưu bằng dấu `;` thì vẫn được.
- Mở bằng **Google Sheets**: *File → Import*. Điền xong chọn *Tệp → Tải xuống → CSV*, rồi **đổi tên lại** đúng `cham-tay-A.csv` hoặc `cham-tay-B.csv`.
- Gửi riêng cho Ân. Có thắc mắc về cách chấm thì hỏi Ân, đừng hỏi người chấm kia.

Phiếu chỉ chứa dữ liệu giả lập. Nhóm chỉ ghi vai của bạn vào báo cáo, ví dụ "học viên ngoài nhóm", không ghi tên trừ khi bạn đồng ý.
