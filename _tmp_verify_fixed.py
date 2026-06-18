import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

check_ids = [334, 335, 336, 470, 587, 588, 597, 627, 632, 634]
all_ok = True
for b in books:
    if b["id"] not in check_ids:
        continue
    ok = short = long_ = 0
    for t in b.get("thoughts", []):
        s = len(t["title"]) + len(t["example"])
        if s < 700: short += 1
        elif s <= 900: ok += 1
        else: long_ += 1
    status = "OK" if short == 0 and long_ == 0 else "PROBLEM"
    if status == "PROBLEM": all_ok = False
    print(f"  [{b['id']}]: OK={ok} short={short} long={long_} {status}")
print(f"\nAll OK: {all_ok}")
