"""Reproduce keyword counts on the saved, anonymized two-sentence sample."""
from collections import Counter
import csv
import json
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parent
RULES_VERSION = "keywords-v1"
PATTERNS = {
    "support": r"ho tro|khieu nai|tong dai|cskh|cham soc khach|giai quyet|xu ly|phan hoi",
    "refund": r"hoan tien|hoan lai tien|boi thuong|tra lai tien",
    "delay": r"giao (?:hang )?(?:cham|tre|lau)|giao qua (?:cham|tre)|doi|cho lau|ghep don|giao muon|(?:\d+|mot|hai|ba) tieng|tre hon",
    "cancel": r"huy|huy don",
    "missing_wrong": r"thieu mon|sai mon|giao thieu|nham mon|khong nhan duoc don|khong giao hang",
    "fees_promotions": r"phi|gia|voucher|ma giam|khuyen mai|hoi vien",
}


def normalize(text):
    return "".join(c for c in unicodedata.normalize("NFD", text.lower().replace("đ", "d"))
                   if unicodedata.category(c) != "Mn")


def classify(row):
    text = normalize(row["excerpt"])
    labels = [name for name, pattern in PATTERNS.items() if re.search(r"\b(?:" + pattern + r")\b", text)]
    food = row["app"] == "shopeefood" or bool(re.search(r"\b(?:do an|mon an|grabfood|quan|dat mon|ca vien|tra sua|com|bun|pho|chao|giao hang|giao nhanh|ship|don)\b", text))
    ride = bool(re.search(r"\b(?:cuoc xe|dat xe|goi xe|chuyen xe|grabcar|grabbike|xe om|tai xe.*cho toi|don khach)\b", text))
    context = "mixed" if food and ride else "food" if food else "ride" if ride else "unclear"
    return {**row, "context": context, "labels": ";".join(labels),
            "support_or_refund_mention": int(bool(set(labels) & {"support", "refund"})),
            "food_support_signal": int(context == "food" and bool(set(labels) & {"support", "refund"})),
            "label_method": RULES_VERSION}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    with (ROOT / "reviews.csv").open(encoding="utf-8", newline="") as f:
        rows = [classify(row) for row in csv.DictReader(f)]
    with (ROOT / "reviews-labeled.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    groups = {}
    for name in ["all", "shopeefood", "grab"]:
        subset = rows if name == "all" else [r for r in rows if r["app"] == name]
        n = len(subset)
        labels = Counter(label for row in subset for label in row["labels"].split(";") if label)
        groups[name] = {"n": n, "ratings": dict(Counter(row["rating"] for row in subset)),
                        "contexts": dict(Counter(row["context"] for row in subset)),
                        "keyword_mentions": dict(labels),
                        "support_or_refund": sum(row["support_or_refund_mention"] for row in subset),
                        "food_support_signal": sum(row["food_support_signal"] for row in subset)}
    result = {"rules_version": RULES_VERSION, "denominator": "Every retained review, all star ratings",
              "groups": groups, "hypothesis_threshold": 5,
              "hypothesis_signal_observed": groups["all"]["food_support_signal"] >= 5,
              "limits": "Keyword mentions are screening signals, not verified incidents; categories overlap. No independent human coding. Context inference may be wrong; inspect examples."}
    (ROOT / "counts.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
