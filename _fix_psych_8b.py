import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

appends = {
    614: {
        8: " Мелкие акты нравственной смелости в обычной жизни — тренировка на случай когда ставки высоки.",
    },
    615: {
        4: " Сакс описывает нескольких пациентов с синдромом Туретта которые стали музыкантами или художниками — дефицит контроля трансформировался в особый ритм и спонтанность.",
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

print("=== VERIFY psych_8b ===")
check_ids = {614, 615}
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
