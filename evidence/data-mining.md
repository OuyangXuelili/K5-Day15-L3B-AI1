# Đào data — cách đếm và kết quả

## 1. Kế hoạch mẫu và thời điểm

Kế hoạch được commit ở `1b5ce51` trước lượt thu thập chính thức; có thừa nhận đã xem thử feed ở bước thăm dò. Ngày thu: **27/11/2026**, timestamp UTC của bản lưu: `2026-11-27T03:12:54.718993+00:00`. Không gọi đây là nghiên cứu chưa từng nhìn dữ liệu.

Chọn 75 review mới nhất mỗi app ShopeeFood và Grab trên App Store Việt Nam, `mostrecent`, tối đa hai trang, mọi mức sao; khử trùng theo ID trong từng app. Giữ cả review tích cực, không liên quan và ngữ cảnh chưa rõ. Không thu tên người viết; trích tối đa hai câu của phần nội dung, bỏ liên hệ và định danh. Review là lời người viết, chưa được xác minh sự cố.

## 2. Đọc rồi đặt nhãn

Đọc 30 dòng thăm dò (15 mỗi app), thấy nhóm giao chậm/ghép đơn, hủy đơn, hỗ trợ, hoàn tiền, phí/khuyến mãi và nhận xét chung. Sau đó ghi quy tắc trong `count.py`. Trong lúc rà đã sửa lỗi khớp từ không có ranh giới (ví dụ `hỗ trợ` không được khớp bên trong `đồng hồ trong`) và chuẩn hóa cách cắt tối đa hai câu, rồi chạy lại toàn bộ mẫu. Chưa có hai người gắn nhãn độc lập.

Nhãn tự động là **nhắc từ khóa**, không phải xác nhận người viết bị lỗi dịch vụ:

| Nhãn | Nội dung phát hiện |
|---|---|
| support | hỗ trợ, khiếu nại, tổng đài, CSKH, chăm sóc khách, giải quyết, xử lý, phản hồi |
| refund | hoàn tiền, hoàn lại tiền, bồi thường, trả lại tiền |
| delay | cụm giao chậm/trễ, đợi, chờ lâu, ghép đơn, số giờ chờ; regex hiện bỏ sót một số cách nói tự nhiên |
| cancel | hủy/huỷ sau chuẩn hóa dấu |
| missing_wrong | thiếu/sai/nhầm món hoặc không nhận đơn/không giao hàng |
| fees_promotions | phí, giá, voucher, mã giảm, khuyến mãi, hội viên |

Ngữ cảnh Grab được suy từ từ khóa: đồ ăn, gọi xe, cả hai, hoặc chưa rõ. Đây là suy luận tự động, không coi mọi review Grab là giao đồ ăn. Có review đăng ở app này nhưng nhắc app khác; chỉ tính là nội dung trong nguồn review, không kết luận sự cố thuộc nền tảng nào.

## 3. Kết quả tái tạo được

| Tín hiệu | ShopeeFood (N=75) | Grab (N=75) | Tổng (N=150) |
|---|---|---|---|
| Nhắc hỗ trợ hoặc hoàn tiền | 6/75 (8,00%) | 12/75 (16,00%) | 18/150 (12,00%) |
| Nhắc hỗ trợ/hoàn tiền, được gắn ngữ cảnh đồ ăn | 6/75 (8,00%) | 5/75 (6,67%) | 11/150 (7,33%) |
| Nhắc giao chậm/chờ/ghép đơn | 23/75 (30,67%) | 16/75 (21,33%) | 39/150 (26,00%) |
| Nhắc phí/giá/khuyến mãi | 8/75 (10,67%) | 6/75 (8,00%) | 14/150 (9,33%) |

Mẫu số chính luôn là toàn bộ review giữ lại, không chỉ những review phàn nàn. Các nhãn có thể chồng lặp, không cộng các hàng thành tổng người. Mẫu có 104 review 1 sao, 39 review 5 sao, 2 review 2 sao và 5 review 3 sao. Giả thuyết tìm ≥5 tín hiệu ngữ cảnh đồ ăn đạt ở mức sàng lọc (11/150), không chứng minh tác động của giải pháp.

**Rà lại nhãn sau lần đếm:** `missing_wrong` là 2/150 lần khớp từ khóa. Đối chiếu hai dòng cho thấy một dòng nói không nhận được đơn (`grab:14831270605`), còn một dòng nói về yêu cầu trả thêm phí/không giao hoặc tự hủy (`shopeefood:14827912775`), không mô tả thiếu hoặc giao sai món. Rà lại các excerpt theo nhóm từ khóa thiếu/sai/nhầm món không thấy review nào mô tả thiếu hoặc giao sai món: **0/150 review có tín hiệu thiếu/sai món trong lần rà mục tiêu**. Đây là rà soát có mục tiêu theo từ khóa, chưa phải gắn nhãn tay độc lập toàn bộ 150 dòng; không dùng 2/150 làm bằng chứng cho pain thiếu/sai món.

Regex `delay` bỏ sót ít nhất hai ví dụ trong mẫu ShopeeFood: `14832318194` (“Giao hàng thì lâu…”) và `14832175871` (“Giao đơn lúc nào cũng ghép…”). Do đó 39/150 là số máy đếm theo từ khóa hiện tại, không phải số đầy đủ mọi review có ý giao chậm/chờ/ghép. Chưa tính lại một tỷ lệ thủ công cho toàn bộ mẫu; không cộng tùy ý các dòng bỏ sót vào số 39.

## 4. Sáu ví dụ nguyên văn

Đã đối chiếu ID và đoạn trích của cả sáu ví dụ dưới đây với `reviews.csv`; các câu là nội dung trong mẫu, không phải lời đã xác minh độc lập.

- `shopeefood:14824487759` (2026-11-23T05:12:31-07:00): “Nên để thẳng số của quán cần gì thì gọi thẳng luôn, cứ nhắn với con tép r đợi nch với nv hỗ trợ tốn hết cả thgian ai rảnh đâu mà canh. Mỗi lần cần xử lý là ngồi đợi ngồi canh tốn thgian vch ra” — [nguồn](https://itunes.apple.com/vn/rss/customerreviews/page=1/id=1137866760/sortby=mostrecent/json).
- `shopeefood:14815432527` (2026-11-20T22:50:01-07:00): “Bắt khách hàng đợi quá lâu và xảy ra quá nhiều lần. Không có chính sách chăm sóc khách hàng rõ ràng” — [nguồn](https://itunes.apple.com/vn/rss/customerreviews/page=1/id=1137866760/sortby=mostrecent/json).
- `shopeefood:14804196680` (2026-11-18T01:55:29-07:00): “Tôi thấy Shoppee Food muốn thu tiền khách thanh toán thẻ đơn trước khi nhận đơn, nhưng lại xử lý chậm chạp và thiếu trách nhiệm khi đơn xảy ra tình trạng lỗi trừ tiền nhưng đơn lại báo đã huỷ. Khi chat support thì ko có bất kì 1 ai hỗ trợ, ko có hotline và không được đảm bảo tiền đã bị trừ từ thẻ” — [nguồn](https://itunes.apple.com/vn/rss/customerreviews/page=1/id=1137866760/sortby=mostrecent/json).
- `grab:14831270605` (2026-11-24T20:16:36-07:00): “Không nhận được đơn đồ ăn nhưng khiếu nại mấy ngày k phản hồi không giải quyết” — [nguồn](https://itunes.apple.com/vn/rss/customerreviews/page=1/id=647268330/sortby=mostrecent/json).
- `grab:14828290352` (2026-11-24T04:01:29-07:00): “app nên thêm phần huỷ đơn hàng nữa nha :))) lần nào đặt đồ cũng nửa tiếng không có ship :)) cũng chả huỷ được đơn, cần hỗ trợ thì AI trả lời chả giúp gì được” — [nguồn](https://itunes.apple.com/vn/rss/customerreviews/page=1/id=647268330/sortby=mostrecent/json).
- `grab:14828614082` (2026-11-24T05:37:04-07:00): “Tài xế giao gần 3 tiếng không tới nơi dù chỉ cách 3km, không hủy được đơn, cũng k có tổng đài call nếu ngoài khung giờ 22h-7h sáng. Hỗ trợ KH quá tệ” — [nguồn](https://itunes.apple.com/vn/rss/customerreviews/page=1/id=647268330/sortby=mostrecent/json).

## 5. Chạy lại

```bash
python evidence/count.py
```

Lệnh đọc `reviews.csv` đã cố định để tái tạo `reviews-labeled.csv` và `counts.json`. Nguồn và hash từng trang feed: `review-sources.json`. Muốn thu mẫu mới: `python evidence/collect_reviews.py --cache <thu-muc-ngoai-repo>`; feed mới thay đổi theo thời gian, không thay mẫu đang dùng sau khi chốt. Raw feed chỉ được cache ngoài repo.

## 6. Giới hạn

Không suy tỷ lệ review thành tỷ lệ mọi khách hàng hoặc tỷ lệ khiếu nại/tháng. Hai app là nguồn đối chiếu trong cùng một phương pháp lấy mẫu, không phải hai phương pháp độc lập, và cùng chịu thiên lệch người tự viết review. Trích hai câu có thể mất ngữ cảnh. Regex bỏ sót tiếng lóng, sai chính tả và có thể gắn nhầm ngữ cảnh. Chưa có phỏng vấn, khảo sát hoặc kiểm nhãn độc lập toàn bộ 150 dòng; không khẳng định biết động cơ hay thời gian xử lý thực tế của hãng.
