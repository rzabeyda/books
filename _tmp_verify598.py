import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

short = ok = long_ = 0
for b in books:
    if b["id"] != 598:
        continue
    for i, t in enumerate(b.get("thoughts", [])):
        total = len(t["title"]) + len(t["example"])
        if total < 700:
            short += 1
            print(f"  SHORT [{i}] {total}")
        elif total <= 900:
            ok += 1
        else:
            long_ += 1
            print(f"  LONG [{i}] {total}")

print(f"Book 598: OK={ok}, short={short}, long={long_}")
