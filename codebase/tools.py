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


FOOD_SAFETY = r"\b(?:di ung|ngo doc|di vat|kho tho|sung moi|cap cuu)\b"
# Từ phủ định đứng ngay trước dấu hiệu khẩn ("không bị dị ứng") thì không tính là khẩn.
NEGATION = re.compile(r"\b(?:khong|ko|k|chua|cha|chang|hong)(?:\s+(?:he|co|bi|thay))*\s*$")
PROMPT_INJECTION = (
    r"bo qua (?:moi )?(?:chinh sach|huong dan|quy tac)|system prompt|\[\s*(?:system|he thong)"
    r"|(?:lenh|ghi chu|thong bao|chi thi) (?:cua )?he thong|che do (?:kiem thu|test|debug|admin|nha phat trien|developer)"
    r"|tu (?:dong )?duyet|\brm -|\bexec\(|khoa (?:quan|shop)|phat tai xe|chuyen tien that|tu hoan tien"
    r"|(?:toi|em|minh|tao) la (?:quan ly|admin|quan tri|nhan vien (?:he thong|cskh|ho tro))"
    r"|ignore (?:all |the )?(?:previous|system) instructions|developer mode")


def safety_issue(text):
    text = normalize(text)
    if any(not NEGATION.search(text[:m.start()]) for m in re.finditer(FOOD_SAFETY, text)):
        return "food_safety"
    if re.search(r"so dien thoai|\bsdt\b|dia chi (?:cua )?(?:khach|tai xe|shipper|nguoi)|mat khau|\botp\b|so the|email cua", text):
        return "privacy"
    if re.search(PROMPT_INJECTION, text):
        return "out_of_scope"
    return None


GENERIC_WORDS = {'mau', 'mon', 'phan', 'suat', 'hop', 'ly', 'coc', 'chai', 'nuoc'}


def item_aliases(item, order=None):
    """Tên đầy đủ, tên bỏ chữ "mẫu", và chữ đầu của tên khi chữ đó chỉ có ở một món trong đơn
    (vd "bún" cho "Bún bò" nếu đơn không có món bún khác)."""
    name = normalize(item['name'])
    aliases = [name, name.removesuffix(' mau')] if name.endswith(' mau') else [name]
    first = name.split()[0]
    if order and len(first) >= 3 and first not in GENERIC_WORDS and \
            sum(normalize(other['name']).split()[0] == first for other in order['items']) == 1:
        aliases.append(first)
    return list(dict.fromkeys(aliases))


def mentioned_items(text, order, item_ids):
    """Giữ item_ids của model chỉ khi khách thật sự nhắc từng món (mã hoặc tên) và món có trong đơn.
    Có món không khớp thì trả [] để hệ thống hỏi lại, không gán lời khách sang món khác."""
    if not order or not item_ids:
        return []
    value = normalize(text)
    lookup = {item['item_id']: item for item in order['items']}
    for item_id in item_ids:
        item = lookup.get(item_id)
        if item is None:
            return []
        names = [item_id.lower(), *item_aliases(item, order)]
        if not any(re.search(r'\b' + re.escape(name) + r'\b', value) for name in names):
            return []
    return list(dict.fromkeys(item_ids))


QUANTITY_UNIT = r'(?:phan|suat|ly|coc|chai|mon|hop|cai|to|bat|dia|goi|lon|chiec|xien|banh)'
NUMBER_WORDS = {'mot': 1, 'hai': 2, 'ba': 3, 'bon': 4, 'tu': 4, 'nam': 5, 'sau': 6,
                'bay': 7, 'tam': 8, 'chin': 9, 'muoi': 10}
NUMBER = r'(-?\d+|(?:' + '|'.join(NUMBER_WORDS) + r')(?=\s))'


def to_number(token):
    return NUMBER_WORDS[token] if token in NUMBER_WORDS else int(token)


def affected_quantities(text, order, issue, item_ids):
    """Read only explicit issue + quantity + item phrases; never infer a whole line."""
    if not order or issue not in ('missing_item', 'wrong_item'):
        return {}
    value = normalize(text)
    cue = r'(?:giao\s+)?thieu' if issue == 'missing_item' else r'(?:giao\s+sai|sai\s+mon|nham\s+mon)'
    quantities = {}
    for item in order['items']:
        if item['item_id'] not in item_ids:
            continue
        names = '|'.join(re.escape(name) for name in [item['item_id'].lower(), *item_aliases(item, order)])
        pattern = (r'\b' + cue + r'\s+(?:toan\s+bo\s+)?' + NUMBER + r'\s*'
                   r'(?:' + QUANTITY_UNIT + r'\s+)?(?:' + names + r')\b')
        found = {to_number(match) for match in re.findall(pattern, value)}
        if found:
            quantities[item['item_id']] = next(iter(found)) if len(found) == 1 else None
    return quantities


def preview_classify(text, order=None):
    """Deterministic preview only; this is not an AI prediction or evaluation."""
    value = normalize(text)
    issue = safety_issue(text)
    if not issue:
        rules = [("payment", r"tru tien|tru hai lan|thanh toan.*hai|cho hoan|tien.*chua ve|khau tru|doi soat"),
                 ("missing_item", r"thieu mon|thieu.*(?:com|canh|tra|\bi\d{2}\b)|giao thieu|thieu\s+(?:toan bo\s+)?-?\d+"),
                 ("wrong_item", r"sai mon|giao sai|nham mon"),
                 ("not_received", r"khong nhan|chua nhan|khong thay don|chua co do an|chua giao"),
                 ("cancel_request", r"huy don|xin huy|muon huy|huy giup|khong huy|ko huy|huye|huy duoc"),
                 ("late_delivery", r"cham|tre|ghep don|doi.*tieng|giao lau|nguoi|giao muon")]
        matches = [key for key, pattern in rules if re.search(r"\b(?:" + pattern + r")\b", value)]
        issue = matches[0] if len(matches) == 1 else 'unclear'
        # Payment needs reconciliation even when combined with another complaint.
        if 'payment' in matches:
            issue = 'payment'
    item_ids = list(dict.fromkeys(re.findall(r"\bI\d{2}\b", text.upper())))
    if not item_ids:
        cue = r'\b(?:thieu|giao\s+sai|sai\s+mon|nham\s+mon)\s+(?:mon\s+)?(?:' + NUMBER + r'\s+)?(?:' + QUANTITY_UNIT + r'\s+)?'
        for item in order['items'] if order else []:
            if any(re.search(cue + re.escape(name) + r'\b', value) for name in item_aliases(item, order)):
                item_ids.append(item['item_id'])
    return {"issue": issue, "item_ids": item_ids}


@tool
def check_limit(order, issue, item_ids, item_quantities=None):
    """check_limit · order, issue, item IDs/affected counts · bounded proposal · no writes."""
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
        return decide("need_info", "Không có đơn hợp lệ trong dữ liệu. Vui lòng chọn mã đơn trong danh sách đơn giả lập.", missing=["order_id"])
    if issue == "unclear":
        return decide("need_info", "Bạn gặp giao chậm, thiếu/sai món, chưa nhận đơn, cần hủy hay cần đối soát thanh toán?", missing=["issue"])
    if order["compensated"] or order["payment_status"] != "paid" or issue == "payment":
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
        quantities = item_quantities or {}
        affected = {}
        for item_id in set(item_ids):
            ordered = lookup[item_id]['quantity']
            quantity = quantities.get(item_id, 1 if ordered == 1 else None)
            if type(quantity) is not int or not 1 <= quantity <= ordered:
                return decide('need_info', 'Cần số lượng thiếu/sai hợp lệ của từng món, không tự tính thiếu toàn bộ dòng món. Ví dụ: thiếu 1 phần I01; giao sai 1 phần I02.', missing=['affected_quantity'])
            affected[item_id] = quantity
        amount = sum(quantity * lookup[item_id]['unit_price_vnd'] for item_id, quantity in affected.items())
        if amount > policy["max_refund_vnd"] or amount > order["subtotal_vnd"]:
            return decide("handoff", "Giá trị đề xuất vượt hạn mức tự động; nhân viên phải kiểm tra và duyệt riêng.")
        return decide("draft_refund", "Đề xuất hoàn theo số lượng thiếu/sai đã xác định và đơn giá trong đơn; chỉ là bản nháp chờ nhân viên duyệt.", amount)
    return decide("handoff", "Tạo yêu cầu nhân viên xác minh theo chính sách; chưa hủy đơn, hoàn tiền hoặc gửi thông báo nào.")
