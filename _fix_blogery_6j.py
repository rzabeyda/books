import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

appends_469 = {
    0: " Искренность в публичности — редкость которую аудитория чувствует сразу и не отпускает.",
    1: " Детский восторг — это не слабость. Это суперсила которую мало кто сохраняет во взрослом возрасте.",
    2: " Последовательность без исключений — вот что отличает тех кто остаётся от тех кто исчезает.",
    3: " Выбирать что транслировать — это не ложь. Это осознанная ответственность перед аудиторией.",
    5: " Семейная аудитория — это не узкая ниша. Это самая устойчивая и лояльная аудитория в рунете.",
    6: " Бренд который живёт в сознании людей — единственный актив который не зависит от платформ.",
    7: " Адаптация формы при сохранении сути — это и есть секрет долголетия в публичном пространстве.",
}

for b in books:
    if b["id"] != 469:
        continue
    for i, t in enumerate(b["thoughts"]):
        if i in appends_469:
            t["example"] += appends_469[i]

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))

print("=== VERIFY 6j ===")
for b in books:
    if b["id"] != 469:
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
        print("ID 469: ALL OK")
