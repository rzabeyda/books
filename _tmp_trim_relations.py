import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

ids = [34, 127, 229, 242, 243, 244, 245, 246, 247, 532, 534]
short, ok, trimmed = [], 0, 0

for b in books:
    if b["id"] not in ids:
        continue
    for i, t in enumerate(b.get("thoughts", [])):
        total = len(t["title"]) + len(t["example"])
        if total < 700:
            short.append(f"  SHORT [{b['id']}][{i}] {total}: {t['title']}")
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
            trimmed += 1
            ok += 1

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",",":"))

print(f"OK: {ok}, Trimmed: {trimmed}, Short: {len(short)}")
for s in short:
    print(s)
