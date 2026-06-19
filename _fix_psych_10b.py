import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

appends = {
    618: {
        4: " Самоосознание включает два компонента: внутреннее (знать свои эмоции и паттерны) и внешнее (знать как тебя воспринимают другие). Большинство людей имеют лишь один из них.",
    },
    640: {
        4: " Тело честнее слов — именно поэтому оговорки жестов важнее оговорок речи.",
        9: " Наука о лжи меняет саму природу разговора — и обязывает к этической осторожности в её применении.",
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

print("=== VERIFY psych_10b ===")
check_ids = {618, 640}
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
