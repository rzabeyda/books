import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

fixes = {
    19: " Победа над собой требует большего мужества чем любое внешнее препятствие.",
    37: " Нет нейтрального ответа — молчание тоже выбор.",
}

count = 0
for b in books:
    if b["id"] != 598:
        continue
    for i, t in enumerate(b.get("thoughts", [])):
        if i in fixes:
            t["example"] += fixes[i]
            total = len(t["title"]) + len(t["example"])
            print(f"[{i}] -> {total}: {t['title']}")
            count += 1

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",",":"))
print(f"Fixed: {count}")
