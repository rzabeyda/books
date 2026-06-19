import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

appends = {
    125: {
        0: " Поток — не мистика. Это описание состояния мозга доступное каждому кто создаёт для него правильные условия.",
        1: " Мастерство без вызова убивает поток так же как вызов без мастерства — оба вектора ведут к нему.",
        6: " Оба состояния — информация о соотношении задачи и навыка, а не приговор о твоих способностях.",
        8: " Обратная связь особенно важна: без неё мозг не знает движется ли он в нужном направлении и где применить усилие.",
    },
    129: {
        6: " Эмоциональное здоровье — не отсутствие негативных эмоций, а способность с ними работать не разрушая себя и отношения.",
        8: " Мозг не заканчивает развиваться в детстве — нейропластичность сохраняется всю жизнь и делает EQ доступным в любом возрасте.",
    },
}

for b in books:
    bid = b["id"]
    if bid not in appends:
        continue
    for i, t in enumerate(b["thoughts"]):
        if i in appends[bid]:
            t["example"] += appends[bid][i]

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))

print("=== VERIFY psych_12b ===")
check_ids = {125, 129}
all_ok = True
for b in books:
    if b["id"] not in check_ids:
        continue
    issues = []
    for i, t in enumerate(b["thoughts"]):
        total = len(t["title"]) + len(t["example"])
        if not (700 <= total <= 800):
            issues.append("t%d=%d" % (i, total))
    if issues:
        all_ok = False
        print("ID %d: %s" % (b["id"], " ".join(issues)))
if all_ok:
    print("ALL OK!")
