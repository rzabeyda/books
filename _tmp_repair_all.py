import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

bad_ids = [126, 334, 335, 336, 470, 587, 588, 597, 598, 627, 632, 634]
repaired = 0
sizes = {}

for b in books:
    if b["id"] not in bad_ids:
        continue
    book_sizes = []
    for i, t in enumerate(b.get("thoughts", [])):
        ex = t["example"]
        q_idx = ex.find("?")
        if q_idx > 5:
            # cut at last clean sentence before the garbage
            clean = ex[:q_idx].rstrip()
            # find last proper sentence ending
            for punct in [". ", "! ", "? ", ".\n"]:
                last = clean.rfind(punct)
                if last > len(clean) // 2:
                    clean = clean[:last+1]
                    break
            t["example"] = clean.rstrip()
            repaired += 1
        total = len(t["title"]) + len(t["example"])
        book_sizes.append((i, total))
    sizes[b["id"]] = book_sizes

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",",":"))

print(f"Repaired: {repaired} thoughts")
for bid, book_sizes in sizes.items():
    short = sum(1 for _, s in book_sizes if s < 700)
    ok = sum(1 for _, s in book_sizes if 700 <= s <= 900)
    long_ = sum(1 for _, s in book_sizes if s > 900)
    print(f"  [{bid}]: OK={ok} short={short} long={long_}")
