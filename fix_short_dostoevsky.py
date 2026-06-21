import json

fixes = {
    681: {
        0: " Это первый в мировой литературе роман о механике политического террора — написан точнее любого аналитика.",
        1: " Это делает «Бесов» бесконечно актуальным текстом."
    },
    682: {
        6: " Это история о человеке, который любит красиво и безнадёжно — вне зависимости от страны и эпохи."
    },
    683: {
        1: " Этот аргумент не устарел: каждое новое утопическое движение проверяется Подпольным человеком на прочность — и проигрывает."
    },
    684: {
        2: " Достоевский первым показал бедность не через факты, а через внутренний монолог человека сохраняющего достоинство."
    },
    685: {
        0: " Аркадий не жаден — он просто не умеет иначе защититься."
    }
}

with open("C:/books/dostoevsky_books.json", encoding="utf-8") as f:
    books = json.load(f)

for b in books:
    bid = b["id"]
    if bid not in fixes:
        continue
    for i, t in enumerate(b["thoughts"]):
        if i in fixes[bid]:
            t["example"] += fixes[bid][i]

with open("C:/books/dostoevsky_books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False)

print("Финальная проверка:")
all_ok = True
for b in books:
    desc_len = len(b["description"])
    issues = []
    if not (125 <= desc_len <= 150):
        issues.append(f"desc={desc_len}")
    for i, t in enumerate(b["thoughts"]):
        total = len(t["title"]) + len(t["example"])
        if not (700 <= total <= 800):
            issues.append(f"t{i}={total}")
            all_ok = False
    print(f"  {b['id']} {b['title']}: desc={desc_len} " + (", ".join(issues) if issues else "OK"))
print("All OK" if all_ok else "ISSUES FOUND")
