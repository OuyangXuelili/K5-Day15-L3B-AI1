# Tóm tắt mô phỏng simulate-1@20261127-144132

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| it_khieu_nai | 52 | 1 | 808 | 22 | 1.0 | 3.0 |
| dung_deu | 29 | 2 | 1611 | 43 | 2.0 | 5.9 |
| can_lien_he_nhieu | 19 | 3 | 2422 | 64 | 3.0 | 8.8 |

Tỉ lệ đạt dùng để tính: 30/30 (100%) — lượt run-2@20261127-143025

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (300 người) | Chi phí / tháng — cơ sở (1.000 người) | Chi phí / tháng — cao (5.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-4o-mini (vào 0.15 · ra 0.6 $/1M) | $0.00022 | $0.00022 | $0.00013 | $0.0864 | $0.2880 | $1.44 | $0.00029 |
| openai/gpt-4o-mini (vào 0.15 · ra 0.6 $/1M) | $0.00022 | $0.00022 | $0.00013 | $0.0864 | $0.2880 | $1.44 | $0.00029 |
| gpt-5-mini (vào 0.25 · ra 2.0 $/1M) | $0.00041 | $0.00041 | $0.00024 | $0.1578 | $0.5261 | $2.63 | $0.00053 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.7) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: openai/gpt-4o-mini. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/100.
