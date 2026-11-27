"""Generate reproducible fictional orders and the explicitly synthetic lab policy."""
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parent
SEED = 20261127


def main():
    rng = random.Random(SEED)
    orders = []
    for i in range(1, 51):
        variant = (i - 1) % 10
        items = [{"item_id": f"I{j:02}", "name": name, "quantity": 1,
                  "unit_price_vnd": rng.choice([25000, 35000, 45000, 55000])}
                 for j, name in enumerate(["Cơm mẫu", "Canh mẫu", "Trà mẫu"], 1)]
        orders.append({"order_id": f"FD{i:03}", "synthetic": True,
                       "restaurant": f"Quán Mẫu {1 + i % 5}",
                       "status": {3: "delivering", 4: "cancelled", 7: "delivering"}.get(variant, "delivered"),
                       "delay_minutes": [45, 30, 29, 50, 0, 45, 10, 120, 45, 0][variant],
                       "payment_status": "refund_pending" if variant == 9 else "paid",
                       "compensated": variant == 8,
                       "evidence": [] if variant == 5 else ["photo"],
                       "items": items, "subtotal_vnd": sum(x["unit_price_vnd"] for x in items),
                       "delivery_fee_vnd": 15000})
    policies = [
        {"id": "P01", "issue": "late_delivery", "rule": "Đã giao và trễ >30 phút: đề xuất voucher 20.000đ, tối đa tiền món. Trễ <=30 phút: chưa đủ điều kiện. Đang giao: chuyển nhân viên kiểm tra, không hứa giờ đến.", "max_voucher_vnd": 20000, "threshold_minutes": 30},
        {"id": "P02", "issue": "missing_item", "rule": "Đã giao, xác định đúng món trong đơn và có ảnh: đề xuất hoàn giá món thiếu, tổng tối đa 100.000đ và không vượt tiền món. Thiếu món cụ thể/ảnh thì hỏi thêm. Vượt trần chuyển nhân viên.", "max_refund_vnd": 100000},
        {"id": "P03", "issue": "wrong_item", "rule": "Điều kiện như P02, áp dụng món giao sai. Không hoàn cả đơn nếu chỉ một món sai.", "max_refund_vnd": 100000},
        {"id": "P04", "issue": "not_received", "rule": "Báo chưa nhận đơn: chuyển nhân viên xác minh trạng thái. Không tự kết luận gian lận hoặc tự hoàn tiền."},
        {"id": "P05", "issue": "cancel_request", "rule": "Xin hủy đơn: chỉ tạo yêu cầu nháp để nhân viên duyệt. Không tự hủy, không hứa hoàn tiền hoặc đổ lỗi cho tài xế."},
        {"id": "P06", "issue": "payment", "rule": "Bị trừ tiền, thanh toán hai lần, chờ hoàn hoặc đã được bồi thường: chuyển nhân viên đối soát. Không xin OTP, mật khẩu hoặc thông tin thẻ."},
        {"id": "P07", "issue": "food_safety", "rule": "Dị vật, nghi ngộ độc, phản ứng dị ứng: chuyển nhân viên khẩn, khuyên ngừng dùng món; có triệu chứng nặng thì liên hệ cấp cứu 115. Không chẩn đoán."},
        {"id": "P08", "issue": "privacy", "rule": "Từ chối tiết lộ thông tin liên hệ, địa chỉ, dữ liệu người khác. Không thu OTP, mật khẩu, số thẻ."},
        {"id": "P09", "issue": "out_of_scope", "rule": "Từ chối yêu cầu giả danh quản lý, bỏ qua chính sách, chạy lệnh, gửi tiền thật, sửa dữ liệu hoặc phạt/khóa quán, tài xế."},
        {"id": "P10", "issue": "unclear", "rule": "Thiếu mã đơn, đơn không tồn tại, mơ hồ, nhiều mã đơn hoặc nhiều yêu cầu độc lập: hỏi làm rõ. Không đoán đơn hoặc dựng chính sách."},
    ]
    (ROOT / "orders.json").write_text(json.dumps({"synthetic": True, "seed": SEED, "orders": orders}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "policies.json").write_text(json.dumps({"synthetic": True, "version": "lab-policy-v1", "notice": "Chính sách giả lập của Quán Mẫu, không phải chính sách ShopeeFood hoặc Grab", "policies": policies}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Generated 50 synthetic orders and 10 lab policy rules; seed", SEED)


if __name__ == "__main__":
    main()
