import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

appends_241 = {
    1: " Быстрый рост — это не только возможность, это ещё и серьёзный стресс-тест.",
    2: " Каждое поколение заслуживает медийных людей которые говорят на его языке по-настоящему.",
    3: " Понимание как работает внимание своей аудитории — ключ к эффективной коммуникации в любом формате.",
    4: " Самобытность начинается там где заканчивается подражание — и именно тогда карьера становится настоящей.",
    5: " Один источник контента и много каналов дистрибуции — самая умная стратегия для роста.",
    6: " Долгосрочность определяется не хайпом который привёл — а качеством что осталось после него.",
    7: " Принципы стареют медленно, конкретные решения — быстро. Именно поэтому учатся принципам а не копируют шаги.",
    8: " Именно в молодом возрасте эти ошибки стоят дороже всего — и именно тогда учат больше всего.",
    9: " Правильный фундамент в начале — самая долгосрочная инвестиция в публичной карьере.",
}

for b in books:
    if b["id"] != 241:
        continue
    for i, t in enumerate(b["thoughts"]):
        if i in appends_241:
            t["example"] += appends_241[i]

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))

print("=== VERIFY 6f ===")
for b in books:
    if b["id"] != 241:
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
        print("ID 241: ALL OK")
