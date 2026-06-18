import json, re
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

bad_ids = [126, 334, 335, 336, 470, 587, 588, 597, 598, 627, 632, 634]
repaired = 0

for b in books:
    if b["id"] not in bad_ids:
        continue
    for i, t in enumerate(b.get("thoughts", [])):
        ex = t["example"]
        # find first run of 2+ consecutive "?" - that's garbage
        m = re.search(r'\?{2,}', ex)
        if not m:
            continue
        idx = m.start()
        # cut back to last clean sentence ending before garbage
        clean = ex[:idx].rstrip()
        for punct in [". ", "! ", "? "]:
            last = clean.rfind(punct)
            if last > len(clean) // 3:
                clean = clean[:last+1]
                break
        t["example"] = clean.rstrip()
        repaired += 1

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",",":"))

print(f"Repaired: {repaired}")
# report sizes
for b in books:
    if b["id"] not in bad_ids:
        continue
    ok = short = long_ = 0
    for t in b.get("thoughts", []):
        s = len(t["title"]) + len(t["example"])
        if s < 700: short += 1
        elif s <= 900: ok += 1
        else: long_ += 1
    print(f"  [{b['id']}]: OK={ok} short={short} long={long_}")
