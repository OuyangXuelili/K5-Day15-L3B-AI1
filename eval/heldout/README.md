# Bộ held-out H01–H10: đo một lần sau lượt 2

**Vì sao có bộ này.** Lượt 2 đạt 30/30, nhưng cải tiến `d860de9` được viết sau khi đọc các câu trượt, và 11 câu đã được chạy thử bằng model thật trong lúc sửa (`eval/report.md` mục 6.5). Bộ này gồm 10 câu mới, chưa từng chạy qua hệ thống, dùng để đo trung thực hơn. Đây là **lượt bổ sung**, không thay cặp lượt 1 → lượt 2 mà rubric chấm.

## Cách dựng

- 8 câu diễn đạt lại từ 8 review trong `evidence/reviews-labeled.csv` chưa dùng trong bộ chính (ngữ cảnh `food`, 1–3 sao); 2 câu tự viết (H07, H08). Mã đơn chọn trong 59 đơn chưa xuất hiện ở bộ chính.
- Câu được chọn để phủ các loại sự cố: giao chậm (đang giao, đã giao >30 phút, đúng 30 phút), huỷ, chưa nhận, thanh toán, thiếu món, an toàn thực phẩm, quyền riêng tư, yêu cầu ngoài phạm vi.
- Đáp án viết tay theo chữ của `data/policies.json` và hồ sơ đơn, rồi đối chiếu với `check_limit` (cùng cách bộ chính dựng expected): khớp cả 10 câu, không phải sửa đáp án nào. Chỉ chạy `check_limit` với nhãn vàng; **chưa chạy model, preview hay agent trên bộ này trước khi commit**.
- Cùng hợp đồng chấm với bộ chính: `eval/grade.py`, `metric_spec.yaml`, cùng `pass_criterion`.

**Giới hạn cần nói rõ:** người soạn (Ân, có trợ lý AI hỗ trợ) đã đọc code và bộ chính, nên bộ này không mù hoàn toàn. Nó mới với code, vì Tú chưa thấy các câu này khi sửa, nhưng chưa phải câu do người ngoài nhóm viết. 10 câu là quá ít để tính tỉ lệ ổn định; chỉ dùng để xem 30/30 có giữ được trên câu mới hay không.

## Quy tắc (ghi trước khi chạy)

1. Commit `heldout.csv`, `heldout-gold.json`, `build_heldout.py`, `run_heldout.py` và file này **trước** khi chạy. `run_heldout.py` từ chối chạy nếu các file chưa commit hoặc code khác bản lượt 2 (`38d67a7`).
2. Chạy **một lần**. Script từ chối chạy lại khi đã có `heldout-run-1.csv`.
3. Không sửa code, prompt hay nhãn vàng sau khi xem kết quả. Nếu nhóm cho rằng một nhãn vàng sai, ghi ý kiến vào báo cáo, giữ nguyên số đo.
4. Kết quả báo cáo riêng trong `eval/report.md`, không cộng vào 30/30.

## Dự đoán (ghi trước khi chạy)

- Tổng **8/10**, khoảng 7–10.
- Rủi ro cao nhất ở các câu mà mẫu chặn của code có thể không bắt, nên phải dựa vào model: H10 (đòi khoá tài khoản tài xế), H09 (đòi địa chỉ nhà tài xế), H08 (con gián trong tô, không dùng chữ "dị vật").
- H07 phụ thuộc việc nhận "canh" thành món "Canh rau"; H03 là biên đúng 30 phút, tiền do code tính nên rủi ro thấp.
- 0 trả thừa, 0 vượt trần, 0 giao dịch thật.

## Lệnh

```bash
python3 eval/heldout/run_heldout.py
```

Sinh `heldout-run-1.csv`, `heldout-run-1.jsonl` và `heldout-summary.md` trong thư mục này; cả ba đều phải commit.
