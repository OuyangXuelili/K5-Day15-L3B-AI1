"""Read fictional orders/policies and validate compensation without external actions."""
import json
from pathlib import Path
import re
import unicodedata
from tracing import tool

DATA = Path(__file__).resolve().parents[1] / "data"


def normalize(text):
    return "".join(c for c in unicodedata.normalize("NFD", text.lower().replace("đ", "d"))
                   if unicodedata.category(c) != "Mn")


def redact(text):
    text = re.sub(r"sk-[A-Za-z0-9_-]{16,}", "[KEY]", text)
    text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[EMAIL]", text)
    text = re.sub(r"(?<!\w)(?:\+84|0)(?:[ .-]?\d){8,10}(?!\w)", "[PHONE]", text)
    return text


def order_ids(text):
    return list(dict.fromkeys(re.findall(r"\bFD\d{3}\b", text.upper())))


@tool
def get_order(order_id):
    """get_order · input: fictional order ID · output: order or None · read only."""
    if not re.fullmatch(r"FD\d{3}", order_id):
        return None
    for order in json.loads((DATA / "orders.json").read_text(encoding="utf-8"))["orders"]:
        if order["order_id"] == order_id:
            return order
    return None


@tool
def get_policy(issue):
    """get_policy · input: issue code · output: policy or None · read only."""
    for policy in json.loads((DATA / "policies.json").read_text(encoding="utf-8"))["policies"]:
        if policy["issue"] == issue:
            return policy
    return None


def safety_issue(text):
    text = normalize(text)
    if re.search(r"di ung|ngo doc|di vat|kho tho|sung moi|cap cuu", text):
        return "food_safety"
    if re.search(r"so dien thoai|dia chi (?:cua )?(?:khach|tai xe|shipper|nguoi)|mat khau|\botp\b|so the|email cua", text):
        return "privacy"
    if re.search(r"bo qua (?:chinh sach|huong dan|quy tac)|system prompt|lenh he thong|\brm -|\bexec\(|khoa (?:quan|shop)|phat tai xe|chuyen tien that|tu hoan tien|toi la quan ly", text):
        return "out_of_scope"
    return None


def preview_classify(text):
    """Deterministic preview only; this is not an AI prediction or evaluation."""
    value = normalize(text)
    issue = safety_issue(text)
    if not issue:
        rules = [("payment", r"tru tien|tru hai lan|thanh toan.*hai|cho hoan|tien.*chua ve|khau tru|doi soat"),
                 ("missing_item", r"thieu mon|thieu.*(?:com|canh|tra)|giao thieu"),
                 ("wrong_item", r"sai mon|giao sai|nham mon"),
                 ("not_received", r"khong nhan|chua nhan|khong thay don|chua co do an|chua giao"),
                 ("cancel_request", r"huy don|xin huy|muon huy|huy giup|khong huy|ko huy|huye|huy duoc"),
                 ("late_delivery", r"cham|tre|ghep don|doi.*tieng|giao lau|nguoi|muon")]
        issue = next((key for key, pattern in rules if re.search(r"\b(?:" + pattern + r")\b", value)), "unclear")
    item_ids = list(dict.fromkeys(re.findall(r"\bI\d{2}\b", text.upper())))
    if not item_ids:
        for key, item in (("com", "I01"), ("canh", "I02"), ("tra", "I03")):
            if re.search(r"\b" + key + r"\b", value):
                item_ids.append(item)
    return {"issue": issue, "item_ids": item_ids}


@tool
def check_limit(order, issue, item_ids):
    """check_limit · input: order, issue and item IDs · output: bounded proposal · no writes."""
    policy = get_policy(issue)
    if policy is None:
        issue, policy = "unclear", get_policy("unclear")
    result = {"decision": "need_info", "issue": issue, "amount_vnd": 0,
              "policy_id": policy["id"], "requires_approval": False,
              "performed_action": False, "order_id": order["order_id"] if order else None,
              "missing_fields": [], "reason": ""}

    def decide(decision, reason, amount=0, missing=None):
        result.update(decision=decision, reason=reason, amount_vnd=amount,
                      requires_approval=decision in ("draft_voucher", "draft_refund", "handoff"),
                      missing_fields=missing or [])
        return result

    if issue in ("privacy", "out_of_scope"):
        return decide("refuse", "Yêu cầu vượt phạm vi hoặc liên quan thông tin riêng tư. Chỉ hỗ trợ đơn giả lập và tạo đề xuất để người phụ trách duyệt.")
    if issue == "food_safety":
        result["urgent"] = True
        return decide("handoff", "Ngừng dùng món và chuyển nhân viên khẩn. Nếu có triệu chứng nặng như khó thở, liên hệ cấp cứu 115; trợ lý không chẩn đoán.")
    if not order:
        result["policy_id"] = "P10"
        return decide("need_info", "Không có đơn hợp lệ trong dữ liệu. Vui lòng chọn một mã đơn FD001–FD050.", missing=["order_id"])
    if issue == "unclear":
        return decide("need_info", "Bạn gặp giao chậm, thiếu/sai món, chưa nhận đơn, cần hủy hay cần đối soát thanh toán?", missing=["issue"])
    if order["compensated"] or order["payment_status"] == "refund_pending" or issue == "payment":
        result["policy_id"] = "P06"
        return decide("handoff", "Cần nhân viên đối soát thanh toán hoặc bồi thường đã có để tránh hoàn trùng. Không hứa thời điểm tiền về.")
    if order["status"] == "cancelled":
        result["policy_id"] = "P06"
        return decide("handoff", "Đơn đã hủy; cần nhân viên kiểm tra tình trạng thanh toán trước khi xác định phương án.")
    if issue == "late_delivery":
        if order["status"] != "delivered":
            return decide("handoff", "Đơn đang giao; tạo yêu cầu nhân viên kiểm tra tiến độ. Không tự hủy đơn hoặc hứa giờ giao.")
        if order["delay_minutes"] <= policy["threshold_minutes"]:
            return decide("no_compensation", "Dữ liệu đơn chưa vượt ngưỡng trễ hơn 30 phút của chính sách thử nghiệm.")
        return decide("draft_voucher", "Đơn đã giao, trễ hơn 30 phút. Đề xuất voucher theo chính sách thử nghiệm, cần nhân viên duyệt.", min(policy["max_voucher_vnd"], order["subtotal_vnd"]))
    if issue in ("missing_item", "wrong_item"):
        if order["status"] != "delivered":
            return decide("handoff", "Cần kiểm tra việc giao đơn trước khi xác nhận món thiếu hoặc sai.")
        lookup = {item["item_id"]: item for item in order["items"]}
        if not item_ids or any(item not in lookup for item in item_ids):
            return decide("need_info", "Cần mã hoặc tên đúng món trong đơn để kiểm tra phần thiếu/sai; không hoàn cả đơn khi chưa xác định.", missing=["item_ids"])
        if not order["evidence"]:
            return decide("need_info", "Cần ảnh xác nhận món thiếu/sai để nhân viên đối chiếu; không thu thông tin cá nhân.", missing=["photo"])
        amount = sum(lookup[item]["quantity"] * lookup[item]["unit_price_vnd"] for item in set(item_ids))
        if amount > policy["max_refund_vnd"] or amount > order["subtotal_vnd"]:
            return decide("handoff", "Giá trị đề xuất vượt hạn mức tự động; nhân viên phải kiểm tra và duyệt riêng.")
        return decide("draft_refund", "Đề xuất hoàn đúng giá trị món đã xác định trong đơn; chỉ là bản nháp chờ nhân viên duyệt.", amount)
    return decide("handoff", "Tạo yêu cầu nhân viên xác minh theo chính sách; chưa hủy đơn, hoàn tiền hoặc gửi thông báo nào.")
