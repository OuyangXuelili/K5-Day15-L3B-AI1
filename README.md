# AI1 — Bàn xử lý khiếu nại đơn giao đồ ăn

**L3B · Track D1 · [Thành viên](TEAMS.md)**

Một khách nhập mã đơn và một vấn đề; trợ lý tra đơn/chính sách, phân loại sự cố và trả bước tiếp theo có căn cứ. Bản chạy thử chỉ tạo đề xuất, không hủy đơn, gửi tin hoặc hoàn tiền thật.

## Trạng thái

| Phần | Đã có | Còn lại |
|---|---|---|
| Bằng chứng | 150 review, hai app, cách lấy mẫu, nhãn từng dòng và số đếm tái tạo được | Kiểm nhãn/người dùng độc lập nếu nhóm làm thêm |
| Demo | Web local, giao diện có ảnh minh họa, workflow và kết nối AI thật; video dự phòng được cung cấp riêng trong form | Không kết nối đơn hàng hoặc giao dịch thật |
| Dữ liệu | 80 đơn giả lập, 10 chính sách, seed cố định; thêm các mức biên và số lượng món | Chưa xác minh ảnh thật; dữ liệu hoàn toàn giả lập |
| Đánh giá | Lượt 1: 24/30 → lượt 2: 30/30; bộ 10 câu mới: 9/10; có phân tích lỗi và giới hạn | Chưa có bộ thử do người ngoài nhóm viết |
| Chi phí | Mô phỏng 100 phiên/167 lượt hỏi, 0 lỗi; 3 kịch bản và 2 mức giá | Chưa đo phút tiết kiệm thực tế; giả định cơ sở 5 phút, thận trọng 1 phút |
| Nộp bài | TEAMS, Canvas/spec, hồ sơ đánh giá/chi phí, bốn reflection và PDF 8 trang | Nộp checkpoint và demo trực tiếp theo lịch BTC |

**Hồ sơ CP2 đã có 5 output hiệu chỉnh gọi `openai/gpt-4o-mini` qua OpenRouter**, lưu ở `eval/calibration/`, cùng hai phiếu chấm khớp 5/5. Đây là bước kiểm cách chấm, chưa phải lượt eval chính thức và không dùng để công bố accuracy. Demo mặc định vẫn là `fake`, token 0. Lượt 1 chính thức `run-1@20261127-111429`: **24/30**, chưa đạt chuẩn §7. Lượt 2 `run-2@20261127-143025` sau cải tiến `d860de9` (`docs/cai-tien-luot-2.md`): **30/30**, đạt chuẩn §7, không câu nào hồi quy; bộ thử đã được nhìn khi sửa nên đây là cận trên. Trên 10 câu mới chốt trước khi chạy: **9/10** (`eval/heldout/`). Phân tích: `eval/report.md`.

**Kết luận: Iterate.** Đủ cơ sở thử nội bộ có nhân viên duyệt; chưa đủ cơ sở triển khai cho khách thật. Bản demo sau đo bổ sung kiểm kiểu JSON và kiểm tên món có mô tả khác; 47 kiểm thử offline đạt. Các số 30/30, 9/10 và chi phí là số đo phiên bản trước thay đổi này, không phải phép đo AI lại của bản demo mới. Xem [nghiệm thu](docs/final-review.md).

## Chạy demo local

Python 3.10+, chỉ dùng thư viện chuẩn, không cần pip/Docker/cloud.

```bash
python run.py
```

Mở **http://127.0.0.1:18115**. Nếu muốn đổi cổng, chép `.env.example` thành `.env`, đổi `APP_PORT`, vẫn giữ `MODEL_PROVIDER=fake` khi chưa muốn gọi API. `.env` không đưa lên Git.

Ảnh giao diện preview ban đầu: [demo-preview.jpg](docs/demo-preview.jpg). Giao diện hiện tại đã được cập nhật; ảnh này không phải bằng chứng gọi AI thật.

Thử các tình huống trong giao diện:

- **Giao chậm:** FD001 trễ 45 phút → đề xuất voucher 20.000đ, chờ duyệt.
- **Thiếu món:** FD007 thiếu cơm I01 → đề xuất đúng giá món trong dữ liệu, chờ duyệt.
- **Ép vượt chính sách:** từ chối, không thực hiện giao dịch.
- **Thiếu một phần:** FD061 đặt 3 phần cơm, báo `thiếu 1 phần I01` → đề xuất 35.000đ; chưa rõ số lượng thì hỏi lại.

Đơn, quán, món và chính sách đều hư cấu; ảnh chỉ minh họa, không đại diện chính sách ShopeeFood hoặc Grab. Chế độ preview dùng quy tắc để thử luồng, không phải model AI.

Muốn chạy dòng lệnh: đặt `APP_MODE=cli` trong `.env`, sau đó `python run.py`. Gõ ví dụ `FD001 đơn giao trễ 45 phút`.

## Lệnh kiểm và tái tạo dữ liệu

```bash
python run.py check
python eval/build_benchmark_v2.py --verify
python -m unittest discover -s eval -p "test_*.py"
python evidence/count.py
```

- `run.py check` kiểm cấu trúc benchmark, metric, TEAMS; không xác nhận chấm độc lập, API hoặc đủ mọi tiêu chí rubric.
- Năm tệp `test_*.py` kiểm hợp đồng luồng, giới hạn tiền, dữ liệu, bộ chấm, chẩn đoán và tên hiển thị; đều chạy fake/mock cục bộ. Bộ v2 cố ý có ca preview trượt; không lấy kiểm thử hợp đồng làm accuracy AI.
- `count.py` đếm trên mẫu review đã lưu. `collect_reviews.py --cache <thư-mục-ngoài-repo>` dùng để thu mẫu mới; không thay dữ liệu đã chốt bằng mẫu live.
- `data/generate.py` tái tạo 80 đơn/10 chính sách với seed 20261127, giữ nguyên 50 đơn ban đầu. Không chạy `data/build_benchmark.py`: script đó dựng bộ v1 cũ. Dùng `eval/build_benchmark_v2.py --verify` để kiểm bộ v2 hiện tại, không ghi đè expected. Bộ 24 ca ở `eval/stress-cases.json` dùng phát triển riêng.

## Khi tiếp tục chạy API cho CP3–CP4

Điền `.env` local bằng cấu hình đã thống nhất. Hồ sơ hiệu chỉnh dùng `MODEL_PROVIDER=openrouter`, `MODEL_NAME=openai/gpt-4o-mini`; adapter OpenAI trực tiếp dùng `MODEL_PROVIDER=openai`, `MODEL_NAME=gpt-4o-mini`. Key chỉ nằm trong `.env`; `MAX_OUTPUT_TOKENS=300`. Không bật mode thật khi chưa được phép chi phí cho lượt chạy tiếp theo.

Sau khi đổi `.env`, dừng server bằng Ctrl+C rồi chạy lại; process đang mở không tự nạp cấu hình mới.

```bash
python run.py eval --try
python run.py eval
python eval/grade.py eval/run-1.csv
python run.py score eval/run-1.csv
# Đọc lỗi thật, chọn một cải tiến rồi chạy cùng bộ câu thử.
python run.py eval
python eval/grade.py eval/run-2.csv
python run.py score eval/run-2.csv
python run.py simulate --rate-from eval/run-2.csv
```

Khung đo token từ API usage; không ước lượng. Lỗi kết nối được giữ là lỗi, không thay bằng mock. Giữ nguyên `run.py`, `codebase/tracing.py`, `eval/run_eval.py`, `cost/simulate.py` của BTC.

## Tài liệu và mốc nộp

- [Bằng chứng](evidence/data-mining.md), [tổng hợp](evidence/summary.md), [data card](data/DATA_CARD.md).
- [Canvas](canvas.md), [spec và kiến trúc](spec.md), [hồ sơ đánh giá](eval/README.md), [báo cáo đánh giá](eval/report.md), [chi phí](cost/cost-estimate.md).
- [Thành viên và phần việc](TEAMS.md).
- [Slide trình bày 8 trang](demo-slides.pdf), [bản HTML có ghi chú](slides/demo.html), [nghiệm thu và giới hạn](docs/final-review.md), [reflection từng thành viên](reflection/).
- [Đối chiếu CP1–CP4](docs/final-review.md#đối-chiếu-bốn-checkpoint): đủ tệp không đồng nghĩa đã nộp form hoặc hoàn thành demo trực tiếp. [Cấu hình model hiện tại](docs/connect-model.md).
- CP1 17:00 27/11; CP2 19:30 27/11; CP3 10:00 28/11; CP4 14:30 28/11; bản cuối 23:59 28/11 (GMT+7). Chuẩn đánh giá chốt CP2, giữ nguyên sau đó.
- Nộp từng mốc bằng [Google Form checkpoint của BTC](https://docs.google.com/forms/d/e/1FAIpQLSdFqBLvf--GLbTUQ2vcFkkKDGsgT-LGT7oftBG_x8Pk-gMVwg/viewform). Dùng cùng tên đội, MSSV trưởng nhóm và repo cho cả bốn mốc. Tạo/push repo không đồng nghĩa đã nộp checkpoint.

## Dùng AI vào việc gì

AI hỗ trợ đọc đề, lấy mẫu review công khai, viết code và hồ sơ, tạo dữ liệu giả lập/bộ thử, kiểm tự động và soạn phân công. Quang xác nhận thông tin nhóm. Hồ sơ hiệu chỉnh, hai lượt eval chính thức, mô phỏng 100 phiên và lượt held-out đều đã lưu kết quả/trace. Đợt hoàn thiện sau đo chỉ kiểm offline, không gọi thêm API. [Khai báo chi tiết](docs/ai-usage.md).

## Nguồn đề

Tạo từ [starter-repo](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/tree/6225f90bc65e7751139127abb42bd0ed7241f2de/starter-repo). Đối chiếu [Track D](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/tracks/track-d-ecommerce.md), [guide](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/02-guide.md), [rubric](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/03-rubric.md).
