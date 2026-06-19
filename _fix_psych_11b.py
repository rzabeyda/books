import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

appends = {
    521: {
        2: " Эта разница — ключ к свободе от чужих ожиданий.",
        4: " Это твоя карта — и работа по её составлению только твоя.",
    },
    522: {
        4: " Это не слабость — это реалистичный взгляд на путь к мастерству.",
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

print("=== VERIFY psych_11b ===")
check_ids = {521, 522}
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
