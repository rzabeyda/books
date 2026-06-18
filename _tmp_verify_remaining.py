import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

check_ids = [23, 471, 675]
for b in books:
    if b["id"] not in check_ids:
        continue
    ok = short = long_ = 0
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
    status = "OK" if short == 0 and long_ == 0 else "PROBLEM"
    print(f"[{b['id']}] OK={ok} short={short} long={long_} {status}")
