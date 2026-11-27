# Chi phí khi dùng thật — chưa chạy mô phỏng

**Trạng thái:** đã lưu token API của 5 output hiệu chỉnh cách chấm tại `eval/calibration/outputs.json`, chưa chạy mô phỏng chi phí. Không dùng 5 câu này để suy ra cost/phiên hoặc cost/task thành công. `cost/personas.yaml` đã chuẩn bị 100 phiên, seed 20261127, ba persona, ba kịch bản 300/1.000/5.000 người. Mọi tần suất và quy mô đều ghi rõ tự ước tính, không phải thống kê từ review.

Giá theo bảng chung BTC ngày 25/11/2026: gpt-4o-mini input/output 0,15/0,60 USD trên 1M token; gpt-5-mini 0,25/2,00 USD trên 1M token. [Bảng BTC](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/further-reading/model-prices.md), [nguồn giá](https://developers.openai.com/api/docs/pricing). Đây là giá để mô phỏng, chưa phải chi phí đã thanh toán.

## Lệnh khi có lượt 2 đã chấm và cùng model

```bash
python run.py simulate --try
python run.py simulate --rate-from eval/run-2.csv
```

Lấy token API từ trace của phiên; không quy đổi số chữ. Chép bảng thật từ `simulate-N-summary.md`, ghi rõ đo token trên model nào và tính giá model nào. Lượt của model khác không chứng minh tỷ lệ đạt của model đó.

| Chỉ số | Trạng thái |
|---|---|
| Token vào/ra và cost/phiên | Chưa đo |
| Tỷ lệ đạt lượt 2 | Chưa đo |
| Cost/task thành công | Chưa tính; không lấy tỷ lệ đạt 100% |
| Cost/tháng ba kịch bản, hai mức model | Chưa tính |

Cost/task thành công = cost/phiên ÷ tỷ lệ đạt thật. Khi tỷ lệ đạt bằng 0 thì không có chi phí hữu hạn cho task thành công. Tần suất bình quân dự kiến = 0,50×0,2 + 0,35×1 + 0,15×3 = 0,9 phiên/người/tháng. Nếu tiết kiệm 5 phút/phiên (tự ước tính), impact tiềm năng = 4,5 phút/người/tháng; chưa đo tiết kiệm thật nên chưa kết luận ROI/go.

Mô phỏng hiện lấy input độc lập mỗi lượt, chưa quản lý hội thoại nhiều lượt cùng session. Hosting local = không mua dịch vụ cloud trong bước này, nhưng giờ công người duyệt chưa được tính.
