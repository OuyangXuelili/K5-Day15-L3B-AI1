"""Fictional storefront names for the web demo; evaluation fixtures stay unchanged."""
import re
import unicodedata

from tools import normalize, order_ids


STOREFRONTS = {
    "Quán Mẫu 1": ("Bếp Nhà An", (
        "Cơm gà xối mỡ", "Canh bí đỏ thịt bằm", "Trà đào cam sả")),
    "Quán Mẫu 2": ("Cơm Nhà Góc Phố", (
        "Cơm sườn nướng", "Canh chua cá", "Trà tắc mật ong")),
    "Quán Mẫu 3": ("Bếp Mộc", (
        "Cơm thịt kho trứng", "Canh rong biển thịt bằm", "Trà vải hạt sen")),
    "Quán Mẫu 4": ("Bếp Hương Việt", (
        "Cơm gà rô ti", "Canh cải thịt bằm", "Trà chanh sả")),
    "Quán Mẫu 5": ("Quán An Nhiên", (
        "Cơm bò xào", "Canh nấm đậu hũ", "Trà sen vàng")),
}
PLACEHOLDER_ITEMS = ("Cơm mẫu", "Canh mẫu", "Trà mẫu")


def display_order(order):
    """Copy an order with fictional display names, retaining IDs, amounts and status."""
    restaurant, menu = STOREFRONTS.get(order["restaurant"], (order["restaurant"], ()))
    names = dict(zip(PLACEHOLDER_ITEMS, menu))
    return {**order, "restaurant": restaurant,
            "items": [{**item, "name": names.get(item["name"], item["name"])}
                      for item in order["items"]]}


def resolve_demo_item_names(text, orders):
    """Resolve full display names to item IDs within the single selected order."""
    ids = order_ids(text)
    if len(ids) != 1:
        return text
    order = next((order for order in orders if order["order_id"] == ids[0]), None)
    if order is None:
        return text
    names = {}
    for original, shown in zip(order["items"], display_order(order)["items"]):
        if original["name"] != shown["name"]:
            names[normalize(shown["name"])] = original["item_id"]
    if not names:
        return text
    variants = [variant for item in display_order(order)["items"]
                if normalize(item["name"]) in names
                for variant in (item["name"], normalize(item["name"]))]
    pattern = r"(?<!\w)(?:" + "|".join(
        re.escape(name).replace(r"\ ", r"\s+")
        for name in sorted(set(variants), key=len, reverse=True)) + r")(?!\w)"
    return re.sub(pattern, lambda match: names[normalize(" ".join(match[0].split()))],
                  unicodedata.normalize("NFC", text), flags=re.IGNORECASE)
