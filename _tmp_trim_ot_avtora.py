import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

trim_ids = [470, 588, 597, 627]
count = 0

for b in books:
    if b["id"] not in trim_ids:
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
        count += 1

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",",":"))
print(f"Trimmed: {count}")
