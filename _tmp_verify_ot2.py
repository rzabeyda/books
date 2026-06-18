import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

target_ids = [470, 587, 588, 597, 598, 627]
for b in books:
    if b["id"] in target_ids:
        ok = short = long_ = 0
        for t in b.get("thoughts", []):
            total = len(t["title"]) + len(t["example"])
            if total < 700:
                short += 1
            elif total <= 900:
                ok += 1
            else:
                long_ += 1
        status = "OK" if short == 0 and long_ == 0 else "PROBLEM"
        print(f"  [{b['id']}] genre={repr(b.get('genre','?'))} OK={ok} short={short} long={long_} {status}")
