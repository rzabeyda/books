import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

# Appends for 239 short thoughts
appends_239 = {
    1: " Войти в культуру по-настоящему невозможно сыграть — только прожить.",
    3: " Именно эта публичная работа над собой создаёт образ человека которому доверяют.",
    5: " Это работает в любой сфере где есть аудитория которая хочет не просто смотреть но и расти.",
    6: " Сообщество — это не следствие размера аудитории. Это следствие качества того что создаётся для неё.",
    8: " Evelone прошёл через это и остался — именно это и стало частью его репутации.",
}

for b in books:
    if b["id"] != 239:
        continue
    for i, t in enumerate(b["thoughts"]):
        if i in appends_239:
            t["example"] += appends_239[i]

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))

print("=== VERIFY 6b ===")
for b in books:
    if b["id"] != 239:
        continue
    issues = []
    for i, t in enumerate(b["thoughts"]):
        total = len(t["title"]) + len(t["example"])
        s = "OK" if 700 <= total <= 800 else ("SHORT=%d" % total if total < 700 else "LONG=%d" % total)
        if s != "OK":
            issues.append("t%d %s" % (i, s))
    if issues:
        for x in issues:
            print(x)
    else:
        print("ID 239: ALL OK")
