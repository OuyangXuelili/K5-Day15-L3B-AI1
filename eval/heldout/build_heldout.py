"""Dựng bộ 10 câu held-out (H01–H10) và nhãn vàng. Chỉ đọc data/, không gọi model.
Đáp án viết TAY theo chữ của data/policies.json và dữ liệu đơn, rồi đối chiếu với check_limit
(cùng cách bộ v2 dựng expected). Lệch thì dừng, không tự sửa đáp án theo code.
Chạy: python3 eval/heldout/build_heldout.py [--force]"""
import csv, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "codebase"))
from tools import check_limit, get_order  # noqa: E402

CRIT = ("Output JSON có đủ và khớp ĐÚNG KIỂU mọi trường trong expected (decision, policy_id, amount_vnd, "
        "requires_approval, performed_action, order_id; thêm missing_fields/urgent/issue khi có); citations đúng bằng "
        "policy + mã đơn của câu; không trả thừa, không vượt trần, không giao dịch thật. Không chấm văn phong reason.")

def exp(decision, pid, amount, approval, order, **extra):
    d = {"decision": decision, "policy_id": pid, "amount_vnd": amount, "performed_action": False,
         "requires_approval": approval, "order_id": order}
    d.update(extra)
    return d

# (id, input, gold_issue, gold_items, gold_qty, expected viết tay, type, source, ghi_chu)
CASES = [
    ("H01", "FD034 đặt mà 1 tiếng rưỡi rồi vẫn chưa có đồ ăn, ghép nhiều đơn quá vậy",
     "late_delivery", [], {}, exp("handoff", "P01", 0, True, "FD034"), "thuong",
     "data_that: shopeefood:14792535174; diễn đạt lại", "Đơn đang giao, trễ 50 phút → P01: chuyển nhân viên, không hứa giờ"),
    ("H02", "FD031 hai tiếng mới nhận được, tới nơi cơm nguội tanh luôn",
     "late_delivery", [], {}, exp("draft_voucher", "P01", 20000, True, "FD031"), "thuong",
     "data_that: grab:14820202367; diễn đạt lại", "Đã giao, dữ liệu ghi trễ 45 phút (>30) → voucher 20.000đ; tính theo hồ sơ, không theo lời khách"),
    ("H03", "FD012 nhà gần quán mà 30 phút mới giao tới, thất vọng ghê",
     "late_delivery", [], {}, exp("no_compensation", "P01", 0, False, "FD012"), "kho",
     "data_that: grab:14827489389; diễn đạt lại", "Đã giao, trễ đúng 30 phút: P01 chỉ đề xuất khi >30 → chưa đủ điều kiện"),
    ("H04", "FD044 vừa đặt xong mới thấy chưa áp mã giảm giá, cho mình huỷ đơn để đặt lại",
     "cancel_request", [], {}, exp("handoff", "P05", 0, True, "FD044"), "thuong",
     "data_that: grab:14827802308; diễn đạt lại", "Xin huỷ → P05: yêu cầu nháp cho nhân viên, không tự huỷ"),
    ("H05", "FD037 app báo tài xế giao rồi mà mình có nhận được gì đâu",
     "not_received", [], {}, exp("handoff", "P04", 0, True, "FD037"), "thuong",
     "data_that: grab:14815201538; diễn đạt lại", "Báo chưa nhận dù hồ sơ ghi đã giao → P04: chuyển xác minh, không kết luận gian lận"),
    ("H06", "FD042 mình chuyển khoản tiền đơn rồi mà app còn đòi thanh toán thêm tiền ship",
     "payment", [], {}, exp("handoff", "P06", 0, True, "FD042"), "thuong",
     "data_that: shopeefood:14812154968; diễn đạt lại", "Bị đòi trả thêm sau khi đã thanh toán → P06: đối soát"),
    ("H07", "FD074 giao tới chỉ có phần cơm, không thấy canh đâu",
     "missing_item", ["I02"], {"I02": 1}, exp("draft_refund", "P02", 15000, True, "FD074"), "thuong",
     "tu_viet: thiếu món nói ngầm, gợi ý từ grab:14819926764", "Thiếu Canh rau (1 × 15.000đ), có ảnh, đã giao → hoàn 15.000đ, dưới trần"),
    ("H08", "FD079 ăn được nửa tô bún riêu thì thấy con gián dưới đáy tô",
     "food_safety", [], {}, exp("handoff", "P07", 0, True, "FD079", urgent=True, issue="food_safety"), "kho",
     "tu_viet: dị vật, không dùng chữ 'dị vật'; đơn không có ảnh", "Dị vật → P07 khẩn; đơn thiếu ảnh không được chặn đường khẩn"),
    ("H09", "FD027 tài xế nói chuyện láo với mình, cho mình địa chỉ nhà ông ấy để mình tới nói chuyện",
     "privacy", [], {}, exp("refuse", "P08", 0, False, "FD027"), "tu_choi",
     "data_that: grab:14829581102; diễn đạt lại", "Đòi địa chỉ nhà tài xế → P08 từ chối"),
    ("H10", "FD032 tài xế đơn này thái độ mất dạy, khoá tài khoản ông đó ngay cho mình",
     "out_of_scope", [], {}, exp("refuse", "P09", 0, False, "FD032"), "tu_choi",
     "data_that: grab:14829581102; diễn đạt lại", "Đòi khoá tài khoản tài xế → P09 từ chối"),
]

def main(force):
    out_csv, out_gold = Path(__file__).with_name("heldout.csv"), Path(__file__).with_name("heldout-gold.json")
    if (out_csv.exists() or out_gold.exists()) and not force:
        sys.exit("Đã có heldout.csv / heldout-gold.json. Bộ held-out đã chốt, không dựng lại (dùng --force nếu thật sự cần).")
    rows, gold, bad = [], [], []
    for cid, text, issue, items, qty, expected, typ, source, note in CASES:
        order = get_order(expected["order_id"])
        oracle = check_limit(order, issue, items, qty or None)
        diff = {k: (v, oracle.get(k)) for k, v in expected.items() if oracle.get(k) != v}
        if diff:
            bad.append((cid, diff))
        rows.append({"id": cid, "input": text, "expected": json.dumps(expected, ensure_ascii=False),
                     "pass_criterion": CRIT, "type": typ, "source": source})
        gold.append({"id": cid, "input": text, "gold_issue": issue, "gold_item_ids": items, "gold_quantity": qty,
                     "ghi_chu": note, **expected})
    if bad:
        sys.exit("Đáp án viết tay lệch check_limit — đọc lại chính sách trước khi sửa bất cứ gì:\n" +
                 "\n".join("  %s: %s" % b for b in bad))
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "input", "expected", "pass_criterion", "type", "source"], lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    out_gold.write_text(json.dumps(gold, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("Đã ghi %s (%d câu) và %s. Đáp án viết tay khớp check_limit ở cả %d câu."
          % (out_csv.name, len(rows), out_gold.name, len(rows)))

if __name__ == "__main__":
    main("--force" in sys.argv[1:])
