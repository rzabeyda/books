import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

count = 0
short = 0
ok = 0
for b in books:
    if b["id"] != 598:
        continue
    for i, t in enumerate(b.get("thoughts", [])):
        total = len(t["title"]) + len(t["example"])
        if total < 700:
            short += 1
            print(f"  SHORT [{i}] {total}: {t['title']}")
        elif total <= 900:
            ok += 1
        else:
            max_ex = 900 - len(t["title"])
            ex = t["example"][:max_ex]
            for punct in [". ", "! ", "? "]:
                last = ex.rfind(punct)
                if last > max_ex // 2:
                    ex = ex[:last+1]
                    break
            t["example"] = ex.rstrip()
            count += 1
            new_total = len(t["title"]) + len(t["example"])
            print(f"  TRIM [{i}] {total}->{new_total}: {t['title']}")

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",",":"))
print(f"Trimmed: {count}, OK: {ok}, Short: {short}")
