# AI1 — Bàn xử lý khiếu nại đơn giao đồ ăn

**L3B · Track D1 · [Thành viên](TEAMS.md)**

Một khách nhập mã đơn và một vấn đề; trợ lý tra đơn/chính sách, phân loại sự cố và trả bước tiếp theo có căn cứ. Bản chạy thử chỉ tạo đề xuất, không hủy đơn, gửi tin hoặc hoàn tiền thật.

## Trạng thái

| Phần | Đã có | Còn lại |
|---|---|---|
| Bằng chứng | 150 review, hai app, cách lấy mẫu, nhãn từng dòng và số đếm tái tạo được | Kiểm nhãn/người dùng độc lập nếu nhóm làm thêm |
| Demo | Web local, workflow, công cụ tra cứu, kiểm tiền và rủi ro | Nối thử model thật khi được phép |
| Dữ liệu | 50 đơn giả lập, 10 chính sách, seed cố định | Chưa xác minh ảnh thật; dữ liệu hoàn toàn giả lập |
| Đánh giá | 30 câu, 3 metric đề xuất, script chấm, kiểm hợp đồng offline | Chấm độc lập 5 output; hai lượt eval AI và phân tích lỗi |
| Chi phí | 100 phiên đã cấu hình, 3 persona, 3 kịch bản, 2 mức giá | Token thật, tỷ lệ đạt lượt 2 và bảng cost |
| Nộp bài | Repo Public đúng tên, TEAMS đúng mẫu, Canvas/spec | Phân công, slide/video, reflection và nộp checkpoint |

**Theo yêu cầu của người dùng, chưa gọi API.** Chế độ mặc định là `fake`, token 0, giao diện ghi rõ mô phỏng. Không có số accuracy AI hoặc cost đã đo. Không dùng kết quả offline như kết quả AI thật.

## Chạy demo local

Python 3.10+, chỉ dùng thư viện chuẩn, không cần pip/Docker/cloud.

```bash
python run.py
```

Mở **http://127.0.0.1:18115**. Nếu muốn đổi cổng, chép `.env.example` thành `.env`, đổi `APP_PORT`, vẫn giữ `MODEL_PROVIDER=fake` khi chưa muốn gọi API. `.env` không đưa lên Git.

Ảnh giao diện đã chạy local: [demo-preview.jpg](docs/demo-preview.jpg). Ảnh thể hiện chế độ preview, không phải bằng chứng gọi AI thật.

Thử ba tình huống trong giao diện:

- **Giao chậm:** FD001 trễ 45 phút → đề xuất voucher 20.000đ, chờ duyệt.
- **Thiếu món:** FD007 thiếu cơm I01 → đề xuất đúng giá món trong dữ liệu, chờ duyệt.
- **Ép vượt chính sách:** từ chối, không thực hiện giao dịch.

Đây là dữ liệu/policy của **Quán Mẫu**, không đại diện chính sách ShopeeFood hoặc Grab. Nhánh preview dùng quy tắc để thử luồng, không phải model AI.

Muốn chạy dòng lệnh: đặt `APP_MODE=cli` trong `.env`, sau đó `python run.py`. Gõ ví dụ `FD001 đơn giao trễ 45 phút`.

## Lệnh kiểm và tái tạo dữ liệu

```bash
python run.py check
python eval/test_contracts.py
python evidence/count.py
```

- `run.py check` kiểm cấu trúc benchmark, metric, TEAMS; không xác nhận chấm độc lập, API hoặc đủ mọi tiêu chí rubric.
- `test_contracts.py` chỉ chạy fake và mock cục bộ: kiểm 30 tình huống, trần tiền trên 50 đơn, schema sai, PII, không đọc file tùy ý; không gọi API.
- `count.py` đếm trên mẫu review đã lưu. `collect_reviews.py --cache <thư-mục-ngoài-repo>` dùng để thu mẫu mới; không thay dữ liệu đã chốt bằng mẫu live.
- `data/generate.py` tái tạo 50 đơn/10 chính sách với seed 20261127. `build_benchmark.py` dựng bộ thử trước lượt thật; không chỉnh expected theo output.

## Khi nhóm cho phép dùng API

Điền `.env`: `MODEL_PROVIDER=openai`, `MODEL_NAME=gpt-4o-mini`, `API_KEY` local; `MAX_OUTPUT_TOKENS=300`. Có adapter OpenRouter nhưng chưa gọi thử. Không bật mode thật nếu chưa đồng ý chi phí.

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
- CP1 17:00 27/11; CP2 19:30 27/11; CP3 10:00 28/11; CP4 14:30 28/11; bản cuối 23:59 28/11 (GMT+7). Chuẩn đánh giá chốt CP2, giữ nguyên sau đó.
- Nộp từng mốc tại [trang hackathon](https://ai20k-hackathon.pages.dev/#submit); tạo/push repo không đồng nghĩa đã nộp checkpoint. Cần phân công có tên để hoàn thiện Canvas CP1.

## Dùng AI vào việc gì

AI hỗ trợ đọc đề, lấy mẫu review công khai, viết code và hồ sơ, tạo dữ liệu giả lập/bộ thử, kiểm tự động. Quang xác nhận thành viên và đội trưởng; chưa ghi có thành viên chấm output hoặc phỏng vấn khi chưa thực hiện. Theo yêu cầu người dùng, chưa gọi API và chưa phân công chi tiết. [Khai báo chi tiết](docs/ai-usage.md).

## Nguồn đề

Tạo từ [starter-repo](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/tree/6225f90bc65e7751139127abb42bd0ed7241f2de/starter-repo). Đối chiếu [Track D](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/tracks/track-d-ecommerce.md), [guide](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/02-guide.md), [rubric](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/03-rubric.md).
