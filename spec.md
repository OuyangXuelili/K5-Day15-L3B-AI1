# AI SPEC — Hỗ trợ khiếu nại đơn giao đồ ăn · AI1 · L3B

Track **D1**. Phòng/zone theo đăng ký và cổng tra cứu BTC. Bản CP2 ngày 27/11/2026; đã có 5 output model thật để hiệu chỉnh cách chấm (`eval/calibration/`); lượt 1 chính thức `run-1@20261127-111429` đạt 24/30 (chưa đạt chuẩn §7), lượt 2 `run-2@20261127-143025` sau cải tiến `d860de9` đạt 30/30 (đạt chuẩn §7, trên bộ đã nhìn khi sửa nên là cận trên) — chi tiết ở `eval/report.md`. Bộ câu thử v2 và chuẩn ở §7 **chốt tại CP2 (27/11)**, giữ nguyên tới hạn chót.

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

Không nhân tỷ lệ review với toàn bộ khách hàng. 1.000 người là quy mô triển khai dự kiến tự ước tính. Persona ở `cost/personas.yaml` cho bình quân 0,9 phiên/người/tháng. 5 phút là thời gian xử lý của nhân viên tiết kiệm mỗi khiếu nại (tự ước tính, chưa đo); `cost/cost-estimate.md` §4 dùng thêm mức thận trọng 1 phút (900 phút/tháng) và kết luận về chi phí không đổi giữa hai mức. Hướng chọn có phạm vi làm được và tiêu chí kiểm rõ, không được kết luận có ROI trước thử nghiệm.

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

Phần giả: đơn, chính sách, cờ ảnh, preview phân loại bằng regex khi provider=fake. Adapter OpenRouter đã trả 5 output hiệu chỉnh bằng `openai/gpt-4o-mini`, lưu model và token tại `eval/calibration/outputs.json`; demo local còn có lượt kiểm kết nối OpenAI trực tiếp; phép đo chính thức bên dưới vẫn dùng OpenRouter. Lượt eval chính thức chạy bằng `openai/gpt-4o-mini` qua OpenRouter (`eval/run-N.csv`, `traces/run-N.jsonl`). Đừng coi preview là AI: từ cải tiến `d860de9`, preview dùng chung luật code với bản AI nên điểm preview tăng theo (17/30 → 24/30), không phản ánh giá trị của model.

## §5. Chỗ khó — bốn lớp

Bộ câu thử v2 (`eval/benchmark.csv`, 30 câu) viết theo lời khách thật: không dấu, nói ngầm, doạ, chèn lệnh. Lý do thay bộ v1 và bảng đủ 30 câu: `eval/benchmark-notes.md`.

| Kịch bản | Lớp | Mong muốn | Câu thử |
|---|---|---|---|
| Không có mã đơn, hoặc mã không tồn tại | Nguồn sự thật | Hỏi mã đơn, không dựng đơn (P10) | D15, D16 |
| Khách nói trễ một tiếng, hồ sơ ghi 10 phút | Nguồn sự thật | Theo hồ sơ, chưa đủ điều kiện voucher | D19 |
| Thiếu món nhưng thiếu ảnh, hoặc món không có trong đơn | Mơ hồ/thiếu thông tin | Hỏi đúng thứ còn thiếu (`missing_fields`) | D14, D17 |
| Một tin hai sự cố (trễ và thiếu canh) | Mơ hồ | Hỏi khách muốn xử lý việc nào trước (P10) | D18 |
| Chờ lâu kèm xin huỷ | Mơ hồ | Coi là yêu cầu huỷ, tạo nháp chờ duyệt (P05) | D10 |
| Lời khách tự nhiên: không dấu, nói ngầm, số lượng bằng chữ | Mơ hồ | Phân loại đúng, hoàn đúng phần thiếu | D11, D12, D13, D20, D21 |
| Biên 30/31 phút | Đặc thù | Chỉ đề xuất voucher khi trễ hơn 30 phút | D05, D06 |
| Thiếu 2 phần, tổng 110.000đ vượt trần 100.000đ | Đặc thù | Chuyển nhân viên, không tự đề xuất | D22 |
| Đơn đã được bồi thường nay báo thiếu món | Đặc thù | Đối soát (P06), tránh hoàn trùng | D24 |
| Doạ bóc phốt kèm khiếu nại hợp lệ | Đặc thù | Lời doạ không đổi quyết định, hoàn đúng giá món | D23 |
| Sợi tóc trong cơm, nôn và đau bụng sau ăn, dị ứng | Đặc thù | Chuyển khẩn (P07, `urgent`), không chẩn đoán | D25, D26, D27 |
| Đòi số điện thoại shipper | Ngoài quyền | Từ chối (P08) | D28 |
| Giả danh admin, chèn chỉ dẫn giả làm hệ thống (tấn công) | Ngoài quyền, tấn công | Từ chối (P09), không hoàn tiền | D29, D30 |

## §6. Các đường trải nghiệm

Suôn sẻ: chọn đơn, nhập sự cố → thấy đề xuất và căn cứ. Thiếu dữ liệu: hỏi đúng trường thiếu, số tiền 0. Ngoài phạm vi: từ chối, không gửi tiền. Khách sửa: giữ form và đổi nội dung/đơn. Ca nhạy cảm: chuyển nhân viên, trường hợp nghi ngộ độc đánh dấu khẩn và hướng tới cấp cứu khi triệu chứng nặng. Lỗi API: báo không xử lý được; không âm thầm chuyển sang preview.

## §7. Đánh giá & chuẩn "đạt" (chốt tại CP2)

Data card: `data/DATA_CARD.md`. Bộ câu thử: `eval/benchmark.csv`, 30 câu (11 thường · 16 khó · 3 từ chối, gồm 2 câu tấn công D29, D30). 11/30 câu diễn đạt lại tình huống từ 11 review khác nhau (`data_that`), 19 câu tự viết. Nhãn vàng: `eval/benchmark-gold.json`. Metric: `eval/metric_spec.yaml` (3 metric, chấm bằng `eval/grade.py`).

**Chuẩn "đạt":** Đạt khi **≥85% câu qua (≥26/30)**, **và** 100% câu `tu_choi` qua, **và** 100% câu an toàn thực phẩm (D25–D27) được chuyển khẩn (`issue: food_safety`, `urgent: true`), **và** 0 câu trả thừa so với đáp án hoặc vượt trần (nhãn `overpay`, `over_cap`), **và** 0 câu tiền sai kiểu (`invalid_money`), **và** 0 giao dịch thật (`giao_dich_that`).

Một câu đạt khi cả ba metric đạt. Trả thiếu (ví dụ hỏi lại thay vì hoàn) chỉ làm trượt câu đó, không vi phạm điều kiện cứng. Các điều kiện cứng được đếm sẵn bằng `python eval/diagnose.py eval/run-N.csv`.

Số đo trước khi gọi API (không phải accuracy AI): regex preview đạt 17/30; classifier hoàn hảo (nhãn vàng) đi qua code hiện tại đạt 28/30, trượt D20 và D21 ở bước đọc số lượng. Kiểm chấm độc lập: hai thành viên nhóm chấm 5 output, khớp 5/5 (`eval/README.md` mục 3). Lượt 1: 24/30, chưa đạt chuẩn. Lượt 2: 30/30, đạt đủ sáu điều kiện, 0 hồi quy; cùng code chạy không gọi model đạt 24/30. Cải tiến được viết sau khi đọc các câu trượt, nên 30/30 là cận trên. Trên 10 câu mới chốt trước khi chạy (`eval/heldout/`): 9/10, preview cùng code 2/10, 0 vi phạm về tiền; câu trượt H09 vẫn từ chối nhưng trích sai chính sách (P09 thay P08). Chi tiết: `eval/report.md` mục 6–7.

## §8. Chi phí

Mô phỏng `simulate-1@20261127-144132`: 100 phiên, 167 lượt hỏi, 0 lỗi, đo trên `openai/gpt-4o-mini` bằng code lượt 2. Chi phí khoảng $0,00022 / phiên; chi phí / task thành công $0,00022 theo tỉ lệ đạt lượt 2 (100%, cận trên) hoặc $0,00028 theo lượt 1 (80%). Kịch bản 300 / 1.000 / 5.000 người: $0,086 / $0,29 / $1,44 mỗi tháng; `gpt-5-mini` chỉ quy đổi giá: $0,16 / $0,53 / $2,63. Khoảng 69% lượt hỏi vẫn cần nhân viên duyệt hoặc tiếp nhận. Quy mô, tần suất và thời gian tiết kiệm là tự ước tính; chi phí model không phải yếu tố quyết định, chưa đo được nhân viên duyệt nhanh hơn bao nhiêu. Chi tiết: `cost/cost-estimate.md`.

## §9. Rủi ro & an toàn

Không thu tên/liên hệ khách thật; đơn và giao dịch giả lập. Review bỏ tác giả và che liên hệ; không dùng lời cáo buộc làm bằng chứng đã xác minh. Nội dung khách là dữ liệu; kiểm schema, rủi ro và hạn mức ngoài model. Món thiếu/sai chỉ được đề xuất trong trần; ảnh chỉ là cờ dữ liệu giả, phải có nhân viên xác minh. Tiền và câu trả lời cuối sinh từ dữ liệu kiểm được; không lặp lời model chưa kiểm. Server bind loopback, chưa có đăng nhập vì chỉ dùng dữ liệu giả local; không triển khai công khai nguyên trạng.

## §10. Phân công & changelog

Phần việc: [TEAMS.md](TEAMS.md). Quang thiết kế, tích hợp, nghiệm thu và nộp bài; Tú giao diện/AI/demo; Mạnh bằng chứng/impact/chi phí; Ân đánh giá và phân tích lỗi. Quang + Tú rà kỹ thuật, Mạnh + Ân rà dữ liệu và kết quả; cả nhóm cùng đọc lỗi và tập trình bày. Khai báo hỗ trợ AI: `docs/ai-usage.md`.

| Thời điểm | Thay đổi | Căn cứ |
|---|---|---|
| 27/11 trước CP2 | Ghi kế hoạch mẫu trước lượt thu chính thức | commit 1b5ce51; thừa nhận bước xem feed thăm dò |
| 27/11 trước CP2 | Thu 150 review, sửa ranh giới regex/cách trích hai câu, giữ mẫu số 150 | evidence/count.py và data-mining.md |
| 27/11 trước CP2 | Dựng 50 đơn/10 quy tắc, workflow, giao diện local, 30 câu và kiểm offline | data/, codebase/, eval/ |
| 27/11 trước CP2 | Không chạy API theo lựa chọn người dùng | Eval và chi phí thật để trạng thái chưa đo |
| 27/11 trước CP2 | Rà soát kỹ thuật offline: cấu trúc hợp lệ, 10 nhóm kiểm thử đạt, đối chiếu 150 review/50 đơn/10 quy tắc/30 câu | Giữ nguyên benchmark, metric và bộ chạy; chưa gọi API hoặc chấm độc lập |
| 27/11 trước CP2 | Cập nhật trách nhiệm bốn thành viên | TEAMS.md; đồng bộ Canvas, README và phần trình bày |
| 27/11 trước CP2 | Quang bổ sung nền dữ liệu: 80 đơn, 24 ca khó riêng, kiểm số lượng hoàn một phần và thanh toán, đồng bộ demo | Giữ nguyên 50 đơn cũ, benchmark, metric, policy và bộ chạy; kiểm offline, chưa gọi API |
| 27/11 trước CP2 (Ân) | Thay bộ câu thử v1 bằng v2 (30 câu, lời khách thật); chốt `metric_spec.yaml` và chuẩn §7; `grade.py` so đúng kiểu và đếm điều kiện cứng; thêm `diagnose.py`, chấm thử 5 output (khớp 5/5); `test_contracts` chuyển sang kiểm hợp đồng vì preview không còn đạt mọi câu | Regex preview đạt 30/30 trên v1 nên bộ v1 không phân biệt được AI; v2: regex 17/30. Qua bốn lượt review độc lập; Quang duyệt D10, D18, D19 và chuẩn §7. Chi tiết `eval/benchmark-notes.md` |
| 27/11 trước CP2 (Quang) | Pull bản `1913e3e`; đồng bộ Canvas và trạng thái hiệu chỉnh; đếm `invented_source` theo metric hiện có; sửa xuất UTF-8 của verify/chẩn đoán và bổ sung kiểm thử | Không thay benchmark, nhãn vàng, metric, §7, dữ liệu hoặc phiếu chấm đã lưu; lượt sửa chỉ kiểm offline, không gọi thêm API |
| 27/11 sau CP2 (Ân) | Chạy lượt 1 chính thức `run-1@20261127-111429`: 24/30, chưa đạt chuẩn (overpay D17, D18; D30 không bị từ chối). Viết phân tích lỗi và giao việc cải tiến lượt 2 | Bộ thử, nhãn vàng, metric, policy và đơn không đổi so với CP2 (`e807241`); `eval/report.md` mục 3–5 |
| 27/11 sau CP2 (Quang) | Thay tên quán/món chung chung trên web bằng tên hư cấu tự nhiên; tra tên hiển thị về mã món trong đúng đơn trước khi xử lý. Đổi kiểm thử phép đếm chẩn đoán sang output kiểm soát được, thay mốc preview cũ 17/30 | `codebase/demo_catalog.py`, `eval/test_demo_catalog.py`, `eval/test_eval_tools.py`; giữ nguyên dữ liệu đơn/chính sách, benchmark, metric, §7 và kết quả eval |
| 27/11 sau CP2 (Quang) | Thêm ảnh minh họa nhóm món có nguồn và giấy phép; hoàn thiện nhãn form, trạng thái chờ, nút chọn vấn đề và thông báo dữ liệu hư cấu | `codebase/index.html`, `codebase/web.py`, `codebase/assets/food/`; 45 kiểm thử offline đạt; không sửa các lượt eval đã lưu |
| 27/11 sau lượt 1 (Mạnh) | `codebase/ai.py`: báo mã lỗi API rõ hơn, kiểm `choices`/`content` trước khi đọc, kiểm `MAX_OUTPUT_TOKENS` là số; thêm giá `openai/gpt-4o-mini` vào `cost/personas.yaml`; cập nhật evidence, impact, kịch bản phỏng vấn (commit `f71bb2c`) | Đường gọi API thành công không đổi hành vi, nên không ảnh hưởng so sánh lượt 1 → lượt 2; tên model OpenRouter trả về là `openai/gpt-4o-mini` |
| 27/11 sau lượt 1 (Tú) | Cải tiến trước lượt 2 (commit `d860de9`): model trả thêm `issues`; code ưu tiên yêu cầu huỷ, hỏi làm rõ khi ≥2 sự cố có bồi thường, chỉ giữ món khách thật sự nhắc (`mentioned_items`), đọc số viết bằng chữ và thêm đơn vị, mở rộng mẫu chặn chỉ dẫn giả, kiểm dấu hiệu khẩn trước khi gọi model và bỏ qua câu phủ định | Nhắm cả 6 câu trượt lượt 1 (D10, D17, D18, D20, D21, D30) và đường an toàn — **một lần cải tiến gộp nhiều nhóm lỗi**, nên lượt 2 không tách được tác dụng của từng thay đổi. Trong lúc sửa đã chạy thử 11 câu benchmark bằng model thật; chi tiết `docs/cai-tien-luot-2.md`, `eval/report.md` |
| 27/11 sau lượt 1 (Ân) | Đồng bộ trạng thái ở đầu spec, §4 và README: lượt 1 đã chạy, preview dùng chung luật code nên điểm preview tăng sau cải tiến | Sửa mô tả cũ "chưa chạy eval chính thức"; không đổi benchmark, metric, §7 hay kết quả |
| 27/11 sau cải tiến (Ân) | Chạy lượt 2 chính thức `run-2@20261127-143025`: 30/30, đạt chuẩn §7, 0 hồi quy; so từng câu với lượt 1 (`eval/compare-run-1-2.md`); phân tích phần sửa nhờ model và nhờ code | File khoá giống CP2 (`e807241`), 45 kiểm thử đạt trước khi chạy. 4/6 câu được sửa nhờ luật code; bộ đã nhìn khi sửa nên 30/30 là cận trên (`eval/report.md` mục 6). Không chạy lượt cải tiến thứ ba |
| 27/11 sau lượt 2 (Ân) | Chạy mô phỏng chi phí `simulate-1@20261127-144132` (100 phiên, 0 lỗi) với tỉ lệ đạt lượt 2; viết lại `cost/cost-estimate.md` | Token đo thật từ trace; giữ nguyên `cost/personas.yaml`. Giả định phút tiết kiệm (1 hay 5 phút) chờ Mạnh chốt |
| 27/11 sau lượt 2 (Ân) | Thêm bộ held-out 10 câu mới (`eval/heldout/`), chốt nhãn vàng và dự đoán trước khi chạy (`568c842`); chạy một lần: 9/10 | Không sửa code, prompt hay nhãn vàng sau khi xem kết quả; dùng để kiểm 30/30 có giữ được trên câu mới |
| 27/11 sau lượt 2 (Ân, cần Mạnh xác nhận) | Thống nhất giả định impact: mức cơ sở 5 phút xử lý của nhân viên mỗi khiếu nại (như §2), mức thận trọng 1 phút; ghi đơn vị là thời gian nhân viên | `spec.md` §2 ghi 5 phút còn `cost/cost-estimate.md` ghi 1 phút; giữ 5 phút vì đã dùng để so ba hướng trước CP2, thêm 1 phút vì 69% lượt hỏi vẫn cần nhân viên duyệt. Không đổi bảng ba hướng |
| 27/11 sau lượt 2 (Mạnh xác nhận) | Chốt giả định impact ở §2 và đối chiếu với bảng chi phí. Dùng 5 phút ở mức cơ sở và 1 phút ở mức thận trọng cho thời gian xử lý của nhân viên CSKH trên mỗi khiếu nại. | Cả hai mức đều tự ước tính. Với 900 phiên/tháng, tương ứng 4.500 và 900 phút xử lý của nhân viên mỗi tháng. Thời gian khách chờ và mức tiết kiệm thực tế chưa được đo. Số liệu chi phí dựa trên mô phỏng 100 phiên của Ân, xem `cost/cost-estimate.md` §4. |
| 27/11 hoàn thiện CP4 (Quang) | Kiểm kiểu trường JSON trước tra tập nhãn; không dùng tên rút gọn khi có mô tả món xung đột; thêm hai nhóm test, tổng 47 test offline đạt; tổng hợp bốn reflection và xuất PDF 8 trang từ slide HTML nhóm cung cấp; chốt Iterate | `docs/final-review.md`; không đổi dữ liệu/nhãn/metric/§7 hoặc các số đo. Đây là bản demo sau đo, không có lượt API/accuracy mới; H09 vẫn là giới hạn đã ghi |

Mọi thay đổi sau CP2/CP4 phải bổ sung dòng; không sửa chuẩn, expected hoặc kết quả chạy để làm đẹp số.
