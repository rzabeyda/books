import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

check_ids = [334, 335, 336, 470, 587, 588, 627, 632, 634]
trimmed = 0
for b in books:
    if b["id"] not in check_ids:
        continue
    for t in b.get("thoughts", []):
        total = len(t["title"]) + len(t["example"])
        if total <= 900:
            continue
        max_ex = 900 - len(t["title"])
        ex = t["example"][:max_ex]
        for punct in [". ", "! ", "? "]:
            last = ex.rfind(punct)
            if last > max_ex // 2:
                ex = ex[:last+1]
                break
        t["example"] = ex.rstrip()
        trimmed += 1

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",",":"))

print(f"Trimmed: {trimmed}")
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
    print(f"  [{b['id']}]: OK={ok} short={short} long={long_} {status}")
