import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

for b in books:
    if b["id"] == 232:
        t = b["thoughts"][0]
        old = " Книга написана с иронией и теплотой — Готтлиб не щадит себя и это делает её истории узнаваемыми для любого кто хоть раз задавался вопросом: «А что если моя жизнь могла бы быть другой?»"
        new = " Книга написана с иронией и теплотой — Готтлиб не щадит себя и это делает её истории узнаваемыми для каждого кто хоть раз думал что жизнь могла сложиться иначе."
        t["example"] = t["example"].replace(old, new)
        break

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))

print("=== VERIFY psych_14c ===")
for b in books:
    if b["id"] == 232:
        issues = []
        for i, t in enumerate(b["thoughts"]):
            total = len(t["title"]) + len(t["example"])
            if not (700 <= total <= 800):
                issues.append("t%d=%d" % (i, total))
        if issues:
            print("ID 232: %s" % " ".join(issues))
        else:
            print("ALL OK!")
