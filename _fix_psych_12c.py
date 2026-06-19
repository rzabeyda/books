import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

for b in books:
    if b["id"] == 129:
        t = b["thoughts"][6]
        old = " Эмоциональное здоровье — не отсутствие негативных эмоций, а способность с ними работать не разрушая себя и отношения."
        new = " Эмоциональное здоровье — не отсутствие негативных эмоций, а способность с ними работать не разрушая себя."
        t["example"] = t["example"].replace(old, new)
        break

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))

print("=== VERIFY psych_12c ===")
for b in books:
    if b["id"] == 129:
        issues = []
        for i, t in enumerate(b["thoughts"]):
            total = len(t["title"]) + len(t["example"])
            if not (700 <= total <= 800):
                issues.append("t%d=%d" % (i, total))
        if issues:
            print("ID 129: %s" % " ".join(issues))
        else:
            print("ALL OK!")
