import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

for b in books:
    if b["id"] == 616:
        t = b["thoughts"][9]
        t["example"] += " Трансценденция не для избранных — это направление которое открывается когда личные нужды удовлетворены."
        break

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))

print("=== VERIFY psych_9b ===")
for b in books:
    if b["id"] == 616:
        issues = []
        for i, t in enumerate(b["thoughts"]):
            total = len(t["title"]) + len(t["example"])
            if not (700 <= total <= 800):
                issues.append("t%d=%d" % (i, total))
        if issues:
            print("ID 616: %s" % " ".join(issues))
        else:
            print("ALL OK!")
