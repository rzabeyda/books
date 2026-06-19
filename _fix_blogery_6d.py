import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

appends_240 = {
    0: " Стать мемом — значит навсегда войти в культуру.",
    1: " Первопроходцы задают стандарты которым все остальные потом следуют годами.",
    2: " Папич держал аудиторию именно через эту живую неопределённость каждого эфира.",
    3: " Подлинность нельзя воспроизвести по инструкции — она либо есть либо нет изначально.",
    4: " Именно поэтому прямой человек в публичном пространстве — редкость которую замечают сразу.",
    5: " Умение управлять вниманием через паузы — один из самых недооценённых инструментов публичности.",
    6: " Аутентичность конкретной эпохи — это то что никогда нельзя воспроизвести позже.",
    7: " Те кто принял геймерство раньше других — оказались в правильном месте в правильное время.",
    8: " Нефильтрованность в нужных руках — это суперсила а не недостаток.",
    9: " Папич доказал: настоящее наследие живёт независимо от того выходит ли человек в эфир.",
}

for b in books:
    if b["id"] != 240:
        continue
    for i, t in enumerate(b["thoughts"]):
        if i in appends_240:
            t["example"] += appends_240[i]

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))

print("=== VERIFY 6d ===")
for b in books:
    if b["id"] != 240:
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
        print("ID 240: ALL OK")
