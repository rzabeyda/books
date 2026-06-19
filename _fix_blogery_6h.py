import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

appends_468 = {
    0: " GTA RP доказал: история важнее геймплея — всегда.",
    1: " Именно поэтому к публичности нужно готовиться так же серьёзно как к контенту.",
    2: " Хейт — это топливо для тех кто умеет с ним работать правильно.",
    3: " Именно дисциплина а не талант определяет кто остаётся на вершине надолго.",
    4: " Аутентичность — единственная стратегия которая работает с молодой аудиторией без исключений.",
    5: " Осознать что изменилось — первый шаг к тому чтобы найти новый баланс между работой и радостью от неё.",
    6: " Связи в индустрии растят карьеру быстрее любого алгоритма и надолго.",
    7: " Действие после скандала говорит о человеке больше чем все его слова вместе взятые.",
    8: " Системность — не убивает творчество. Она даёт ему надёжный и долгосрочный фундамент.",
}

for b in books:
    if b["id"] != 468:
        continue
    for i, t in enumerate(b["thoughts"]):
        if i in appends_468:
            t["example"] += appends_468[i]

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))

print("=== VERIFY 6h ===")
for b in books:
    if b["id"] != 468:
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
        print("ID 468: ALL OK")
