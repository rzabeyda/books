import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

for b in books:
    if b["id"] == 131:
        t = b["thoughts"][0]
        old = " Это открытие пришло из наблюдения: никто не рождается жестоким — жестокость это неудовлетворённая потребность."
        new = " Это открытие пришло из наблюдения: никто не рождается жестоким."
        t["example"] = t["example"].replace(old, new)
        break

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))

print("=== VERIFY psych_13c ===")
for b in books:
    if b["id"] == 131:
        issues = []
        for i, t in enumerate(b["thoughts"]):
            total = len(t["title"]) + len(t["example"])
            if not (700 <= total <= 800):
                issues.append("t%d=%d" % (i, total))
        if issues:
            print("ID 131: %s" % " ".join(issues))
        else:
            print("ALL OK!")
