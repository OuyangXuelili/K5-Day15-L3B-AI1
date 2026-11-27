# Chi phí khi dùng thật — mô phỏng 100 phiên sau lượt 2

**Trạng thái:** đã chạy mô phỏng `simulate-1@20261127-144132`: 100 phiên, 167 lượt hỏi, 0 phiên lỗi, toàn bộ gọi `openai/gpt-4o-mini` qua OpenRouter bằng đúng code của lượt 2. Tỉ lệ đạt dùng để tính lấy từ lượt 2 `run-2@20261127-143025` (30/30). File gốc: `cost/simulate-1.csv`, `cost/simulate-1-summary.md`, `traces/simulate-1.jsonl`. Mọi chi phí ở đây là quy đổi theo bảng giá, không phải hoá đơn đã thanh toán.

## 1. Số đo token từ mô phỏng

| Persona | Số phiên | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| it_khieu_nai | 52 | 1 | 808 | 22 | 1,0 | 3,0 |
| dung_deu | 29 | 2 | 1.611 | 43 | 2,0 | 5,9 |
| can_lien_he_nhieu | 19 | 3 | 2.422 | 64 | 3,0 | 8,8 |

Tổng 134.746 token vào và 3.597 token ra. Trung bình mỗi lượt hỏi khoảng 807 token vào và 22 token ra, khớp số đo của lượt 2 (810 / 21,6). Độ trễ model trung bình 1,31 giây mỗi lượt hỏi; phiên chậm nhất 5,4 giây (3 lượt). Token lấy từ `usage` trong trace, không ước lượng.

## 2. Chi phí

| Model (giá $/1M token vào · ra) | Chi phí / phiên | Chi phí / task thành công | Tháng — 300 người | Tháng — 1.000 người | Tháng — 5.000 người |
|---|---:|---:|---:|---:|---:|
| `openai/gpt-4o-mini` (0,15 · 0,60), **đo thật** | $0,00022 | $0,00022 | $0,086 | $0,29 | $1,44 |
| `gpt-5-mini` (0,25 · 2,00), **chỉ quy đổi** | $0,00041 | $0,00041 | $0,16 | $0,53 | $2,63 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Tỉ lệ đạt lượt 2 là 100% nhưng là cận trên, vì bộ thử đã bị nhìn khi cải tiến (`eval/report.md` mục 6.5). **Mức thận trọng** dùng tỉ lệ lượt 1 (80%): $0,00022 ÷ 0,80 ≈ **$0,00028 / task thành công** với `gpt-4o-mini`.
- Dòng `gpt-5-mini` dùng lại số token đo trên `gpt-4o-mini`. Model suy luận thường sinh nhiều token ra hơn và tách token khác, nên con số thật có thể cao hơn. Dòng này chỉ để so mức giá, không phải số đo.
- Số phiên mỗi tháng = 1.000 × (0,50×0,2 + 0,35×1 + 0,15×3) = 900 phiên ở kịch bản cơ sở (tự ước tính).
- Đầu vào mô phỏng lấy ngẫu nhiên từ các câu loại `thuong` và `kho` của bộ thử (27 câu khác nhau). Token là số đo thật, nhưng nội dung không phải lưu lượng khách thật.

## 3. Phần việc vẫn cần nhân viên

Trong 167 lượt hỏi mô phỏng: 62 chuyển nhân viên (`handoff`), 31 nháp voucher và 23 nháp hoàn tiền chờ duyệt, 36 hỏi thêm thông tin, 15 không bồi thường. Như vậy khoảng **69% lượt hỏi vẫn cần nhân viên duyệt hoặc tiếp nhận**. Trợ lý không thay nhân viên; nó tra đơn, đối chiếu chính sách và soạn sẵn đề xuất để nhân viên duyệt nhanh hơn. Tỉ lệ này phản ánh bộ thử (nhiều câu khó), chưa phải tỉ lệ của khách thật.

## 4. So với impact

Chi phí model ở kịch bản cơ sở là **$0,29 / tháng cho 900 phiên**, tức khoảng $0,0003 mỗi phiên. Impact tính bằng **thời gian xử lý của nhân viên** tiết kiệm được mỗi khiếu nại, không tính thời gian chờ của khách. Con số này chưa được đo, nên dùng một mức cơ sở và một mức thận trọng, cả hai tự ước tính:

| Mức | Tiết kiệm / phiên | Impact / người / tháng (0,9 phiên) | Impact / tháng, 1.000 người (900 phiên) | Chi phí model / người / tháng |
|---|---:|---:|---:|---:|
| **Cơ sở** (dùng trong `spec.md` §2 và slide) | 5 phút | 4,5 phút | 4.500 phút ≈ 75 giờ | $0,00029 |
| Thận trọng | 1 phút | 0,9 phút | 900 phút ≈ 15 giờ | $0,00029 |

Vì sao có hai mức: 5 phút là giả định dùng để so ba hướng ở `spec.md` §2 trước CP2. Mô phỏng cho thấy khoảng 69% lượt hỏi vẫn cần nhân viên duyệt hoặc tiếp nhận (mục 3), nên nhân viên vẫn phải đọc lại đề xuất; phần tiết kiệm chỉ là bước tra đơn, đối chiếu chính sách và soạn đề xuất. Vì vậy giữ thêm mức 1 phút làm cận dưới. **Kết luận không đổi giữa hai mức:** chi phí model đều nhỏ hơn rất nhiều so với giá trị thời gian tiết kiệm.

Repo chưa có giá giờ công nhân viên, nên chưa quy đổi thời gian ra tiền. Điểm hoà vốn với chi phí model rất thấp: chỉ cần thời gian tiết kiệm mỗi phiên có giá trị trên khoảng $0,0003. Vì vậy chi phí model không phải điều quyết định go / no-go. Điều quyết định là đề xuất có đúng không (eval) và nhân viên có thật sự duyệt nhanh hơn không (chưa đo). Chưa tính hosting, lưu trữ và giờ công người duyệt.

## 5. Giá và lệnh tái tạo

Giá theo bảng chung BTC ngày 25/11/2026: `gpt-4o-mini` input/output `0,15/0,60 USD trên 1M token`; `gpt-5-mini` `0,25/2,00 USD trên 1M token`. [Bảng BTC](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/further-reading/model-prices.md), [nguồn giá](https://developers.openai.com/api/docs/pricing). Giá dùng để quy đổi, chưa phải chi phí đã thanh toán.

Lệnh đã chạy:

```bash
python run.py simulate --rate-from eval/run-2.csv
```

Chạy lại sẽ sinh lượt `simulate-2`, không ghi đè `simulate-1`.
