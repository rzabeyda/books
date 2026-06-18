import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

appends = {
662: {7: " Взаимное подтверждение двух систем создаёт мощное ощущение достоверности."},
665: {6: " Это прямо прослеживается в акценте на сознательной работе над собой."},
671: {
    4: " Дюси предлагает конкретный алгоритм: рассчитай число жизненного пути ребёнка и выбери имя которое с ним гармонирует.",
    7: " Число — один из элементов принятия решений наряду с опытом и интуицией.",
    9: " Результат — утренний ритуал который создаёт паузу и намерение перед началом дня.",
},
}

count = 0
for b in books:
    bid = b["id"]
    if bid not in appends:
        continue
    for i, t in enumerate(b.get("thoughts", [])):
        if i in appends[bid]:
            t["example"] += appends[bid][i]
            count += 1

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",",":"))
print(f"Fix last: {count}")
