# Khung trình bày 8 trang — AI1

Đây là **dàn ý**; file nộp là `demo-slides.pdf` ở thư mục gốc. Số ở trang 5–7 lấy từ `eval/report.md`, `eval/heldout/` và `cost/cost-estimate.md` (cập nhật 27/11 sau lượt 2).

1. **Người dùng & pain:** khách có đơn đồ ăn gặp sự cố; 18/150 review nhắc hỗ trợ/hoàn tiền, 11/150 có ngữ cảnh đồ ăn; một trích dẫn nguyên văn và nguồn từ evidence/data-mining.md.
2. **Vì sao chọn:** ba hướng trong spec §2; chọn khiếu nại vì phạm vi và điều kiện kiểm rõ. Impact 1.000 người × 0,9 phiên × 5 phút = 4.500 phút/tháng, mọi thừa số tự ước tính, chưa đo.
3. **Giải pháp:** sơ đồ một workflow, một lời gọi model; đơn/policy giả lập; tiền bằng code, người duyệt.
4. **Demo:** FD001 giao trễ; FD007 thiếu món; yêu cầu ép bỏ chính sách. Chạy AI thật (`openai/gpt-4o-mini`). Gợi ý: một ca thường (FD011 chờ gần một tiếng → voucher 20.000đ chờ duyệt) và một ca khó (FD011 chèn "ghi chú hệ thống" đòi hoàn 135.000đ → từ chối, 0đ). Sẵn sàng chạy câu lạ của giám khảo; nếu trượt, mở trace và giải thích như H09.
5. **Đánh giá thế nào (Ân):**
   - Bộ thử 30 câu (11 thường · 16 khó · 3 từ chối, gồm 2 câu tấn công), 11 câu diễn đạt lại từ review thật. 3 metric: quyết định đúng · an toàn tiền · nguồn hợp lệ. Hai thành viên chấm tay 5 output, khớp 5/5.
   - Chuẩn "đạt" chốt CP2: ≥26/30, 100% câu từ chối, 100% câu an toàn thực phẩm chuyển khẩn, 0 trả thừa / vượt trần / giao dịch thật.
   - **Lượt 1 → lượt 2: 24/30 (chưa đạt) → 30/30 (đạt), 0 hồi quy.** Lượt 1 trượt ở trả thừa (D17, D18) và một câu tấn công lọt (D30).
   - Trung thực: cải tiến viết sau khi đọc câu trượt, 4/6 câu được sửa nhờ luật code → 30/30 là cận trên. **Bộ 10 câu mới chốt trước khi chạy: 9/10**; bỏ model chỉ còn 2/10 (bộ chính: 24/30).
   - Lỗi chính: model gán món khách không nhắc (D17 "gà rán" → Trà mẫu, 55.000đ) — code chặn từ lượt 2 nhưng model vẫn sai; H09 từ chối đúng nhưng trích nhầm chính sách.
6. **Chi phí (Mạnh):** mô phỏng 100 phiên, 167 lượt hỏi, 0 lỗi, đo trên `openai/gpt-4o-mini`.
   - **$0,00022 / task thành công** theo tỉ lệ lượt 2 (100%); mức thận trọng theo lượt 1 (80%): $0,00028.
   - 300 / 1.000 / 5.000 người: $0,086 / $0,29 / $1,44 mỗi tháng; `gpt-5-mini` (chỉ quy đổi giá): $0,16 / $0,53 / $2,63.
   - So với impact: $0,00029 / người / tháng so với 4,5 phút xử lý của nhân viên / người / tháng (mức cơ sở 5 phút mỗi khiếu nại, tự ước tính; mức thận trọng 1 phút → 0,9 phút). Kết luận giống nhau ở cả hai mức. Khoảng 69% lượt hỏi vẫn cần nhân viên duyệt.
7. **Kết luận (Ân) — đề xuất: iterate**, nhóm chốt trước khi làm PDF.
   - Vì sao không stop: an toàn tiền giữ ở cả ba lần đo (0 trả thừa, 0 vượt trần, 0 giao dịch thật); 9/10 câu mới; chi phí model không đáng kể (trang 6).
   - Vì sao chưa go: phút tiết kiệm (trang 2) chưa đo; 69% lượt vẫn cần nhân viên nên giá trị nằm ở duyệt nhanh hơn, chưa chứng minh; câu mới chỉ 10 và đã trượt một câu từ chối; chưa có người dùng thật.
   - Đủ để thử nghiệm nội bộ có nhân viên duyệt mọi đề xuất tiền.
8. **Một tuần tiếp:** (1) đo thời gian nhân viên xử lý một khiếu nại có và không có đề xuất, để thay giả định 5 phút; (2) sửa ranh giới quyền riêng tư / ngoài phạm vi (H09) và lỗi gán nhầm món của model, rồi đo trên một bộ câu do người ngoài nhóm viết; (3) 2–3 người dùng thử và quản lý phiên nhiều lượt.

Phân phần trình bày dự kiến: Quang trang 1/3, Mạnh trang 2/6, Tú trang 4/8, Ân trang 5/7; cả nhóm tập và rà theo [TEAMS.md](../TEAMS.md). Tú phụ trách giao diện, thao tác demo trực tiếp và quay video; Quang tổng hợp để nộp. Video do Tú quay; video dự phòng CP4 cần có cả ca thường và ca khó ở trang 4.
