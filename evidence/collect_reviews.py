"""Collect a fixed-size public review sample without author information."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import urllib.request

APPS = {"shopeefood": "1137866760", "grab": "647268330"}


def anonymize(text):
    text = re.sub(r"https?://\S+", "[LINK]", text)
    text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[EMAIL]", text)
    text = re.sub(r"(?<!\w)(?:\+84|0)(?:[ .-]?\d){8,10}(?!\w)", "[PHONE]", text)
    text = re.sub(r"(?i)\b(?:mã đơn|đơn hàng|sđt|biển số)\s*[:#]\s*[A-Za-z0-9.-]+", "[IDENTIFIER]", text)
    return " ".join(text.split())


def excerpt(text):
    sentences = re.split(r"(?<=[.!?])\s+|(?<=[.!?])(?=[A-ZÀ-Ỵ])|[\r\n]+", text.strip())
    return anonymize(" ".join(s for s in sentences if s.strip()) if len(sentences) <= 2
                     else " ".join(sentences[:2]))


def collect(cache, per_app=75):
    cache.mkdir(parents=True, exist_ok=True)
    records, sources = [], []
    for app, app_id in APPS.items():
        seen, accepted = set(), 0
        for page in (1, 2):
            url = f"https://itunes.apple.com/vn/rss/customerreviews/page={page}/id={app_id}/sortby=mostrecent/json"
            cached = cache / f"{app}-{page}.json"
            if cached.exists():
                raw = cached.read_bytes()
            else:
                req = urllib.request.Request(url, headers={"User-Agent": "AI1-public-review-study/1.0"})
                raw = urllib.request.urlopen(req, timeout=30).read()
                cached.write_bytes(raw)
            sources.append({"app": app, "url": url, "sha256": hashlib.sha256(raw).hexdigest(),
                            "fetched_at_utc": datetime.fromtimestamp(cached.stat().st_mtime, timezone.utc).isoformat()})
            entries = json.loads(raw).get("feed", {}).get("entry", [])
            if isinstance(entries, dict):
                entries = [entries]
            for entry in entries:
                if "im:rating" not in entry or "content" not in entry:
                    continue
                review_id = entry["id"]["label"]
                if review_id in seen:
                    continue
                seen.add(review_id)
                if accepted >= per_app:
                    break
                records.append({"review_id": review_id, "app": app,
                                "date": entry.get("updated", {}).get("label", ""),
                                "rating": entry["im:rating"]["label"],
                                "source_url": url,
                                "app_url": f"https://apps.apple.com/vn/app/id{app_id}",
                                "excerpt": excerpt(entry["content"]["label"])})
                accepted += 1
            if accepted >= per_app:
                break
    return records, sources


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, required=True, help="Raw cache outside the public repo")
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "reviews.csv")
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    if args.cache.resolve().is_relative_to(project):
        parser.error("Raw cache must stay outside the repository")
    rows, sources = collect(args.cache)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    manifest = {"collected_at_utc": max(source["fetched_at_utc"] for source in sources),
                "processed_at_utc": datetime.now(timezone.utc).isoformat(),
                "sampling": "75 newest unique review IDs per app, mostrecent pages 1-2, all ratings",
                "count": len(rows), "sources": sources,
                "privacy": "No author names; at most two body sentences; contact details redacted",
                "scope": "Excerpts only; App Store reviewers are not a representative user sample"}
    args.out.with_name("review-sources.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(rows)} anonymized public review excerpts to {args.out}")


if __name__ == "__main__":
    main()
