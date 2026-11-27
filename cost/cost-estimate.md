# Chi phí khi dùng thật — số đo lượt 1 và trạng thái mô phỏng

**Trạng thái:** lượt 1 chính thức `run-1@20261127-111429` đã có số đo token thật từ `traces/run-1.jsonl`, chạy bằng `openai/gpt-4o-mini` qua OpenRouter và đạt 24/30 (80%). Đây là số đo của 30 câu eval, không phải mô phỏng 100 phiên. Chưa có lượt 2 nên chưa dùng tỷ lệ này làm tỷ lệ thành công cuối cùng và chưa chạy `cost/simulate-N.csv`.

## 1. Số đo thật từ lượt 1

| Chỉ số | Giá trị |
|---|---:|
| Số câu | 30 |
| Token vào | 18.905 |
| Token ra | 422 |
| Trung bình token vào/câu | 630 |
| Trung bình token ra/câu | 14 |
| Tỷ lệ đạt lượt 1 | 24/30 (80%) |
| Chi phí quy đổi với gpt-4o-mini | 0,003092 USD / 30 câu |
| Chi phí quy đổi trung bình | 0,000103 USD / câu |

Cách tính theo giá `gpt-4o-mini` input/output `0,15/0,60 USD trên 1M token`:

`(18.905 × 0,15 + 422 × 0,60) / 1.000.000 = 0,00309195 USD`.

Chi phí trên là chi phí quy đổi theo bảng giá, không phải hóa đơn đã thanh toán. Token lấy từ `usage` trong trace, không ước lượng. Lượt 1 chưa đạt chuẩn §7 vì đạt 24/30 thay vì tối thiểu 26/30, còn 2 lỗi overpay và 1 câu từ chối trượt. Không dùng 5 output hiệu chỉnh để thay số đo mô phỏng.

## 2. Cấu hình mô phỏng đã chuẩn bị

`cost/personas.yaml` đã có 100 phiên, seed `20261127`, ba persona, ba kịch bản 300/1.000/5.000 người và các mức giá `gpt-4o-mini`, `openai/gpt-4o-mini`, `gpt-5-mini`. Quy mô người dùng, tỷ lệ persona và tần suất đều là tự ước tính, không suy ra từ 150 review.

Mô phỏng 100 phiên vẫn **chưa chạy** vì cần bản code/model đã chốt, token trace của chính các phiên mô phỏng và tỷ lệ đạt từ lượt 2 cùng model. Không tạo `cost/simulate-N.csv` hoặc số liệu thay thế khi thiếu các điều kiện này.

## 3. Chi phí/task thành công

Công thức: `chi phí trung bình/phiên ÷ tỷ lệ đạt thật`.

Tạm tính theo lượt 1, chỉ để tham khảo trên bộ 30 câu: `0,000103 ÷ 0,80 = 0,000129 USD/task đạt`. Con số này **không phải kết quả cuối**, vì tỷ lệ 80% là lượt 1 và chi phí trung bình đang tính trên câu eval độc lập, không phải 100 phiên mô phỏng theo ba persona.

Tần suất bình quân dự kiến = `0,50×0,2 + 0,35×1 + 0,15×3 = 0,9 phiên/người/tháng` (tự ước tính). Với 1.000 người dùng thử, quy mô tham khảo là 900 phiên/tháng; chưa dùng để kết luận ROI/go vì chưa có cost mô phỏng và chưa đo thời gian xử lý thực tế. Impact hiện chỉ giả định tiết kiệm 1 phút thao tác nhân viên/phiên (tự ước tính), không phải thời gian chờ hay thời gian của khách.

## 4. Giá và lệnh tái tạo

Giá theo bảng chung BTC ngày 25/11/2026: `gpt-4o-mini` input/output `0,15/0,60 USD trên 1M token`; `gpt-5-mini` `0,25/2,00 USD trên 1M token`. [Bảng BTC](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/further-reading/model-prices.md), [nguồn giá](https://developers.openai.com/api/docs/pricing). Giá dùng để quy đổi, chưa phải chi phí đã thanh toán.

Khi có lượt 2 và đủ token trace thật:

```bash
python run.py simulate --rate-from eval/run-2.csv
```

Lệnh sẽ sinh `cost/simulate-N.csv`, `cost/simulate-N-summary.md` và trace mô phỏng. Khi đó chép số đo thật vào tài liệu này, dùng đúng model đã đo và tính cost/task thành công từ tỷ lệ đạt lượt 2. Không sửa kết quả các lượt đã chạy.

Hosting local không tính phí cloud trong bước này; giờ công người duyệt và chi phí vận hành chưa được đo.