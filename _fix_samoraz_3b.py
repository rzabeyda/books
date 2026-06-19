import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

for b in books:
    bid = b["id"]

    if bid == 600:
        # t8=686, need +14
        b["thoughts"][8]["example"] += " Уважай свой стиль."

    if bid == 601:
        # t9=801, over by 1 — trim trailing period
        t = b["thoughts"][9]
        if t["example"].endswith("."):
            t["example"] = t["example"][:-1]

    if bid == 603:
        # t6=687, need +13
        b["thoughts"][6]["example"] += " Идентичность создаёт последовательность."
        # t8=686, need +14
        b["thoughts"][8]["example"] += " Скука — приглашение к творчеству, а не проблема которую нужно немедленно решать."
        # t9=694, need +6
        b["thoughts"][9]["example"] += " Смысл защищает лучше силы воли."

    if bid == 605:
        # t5=697, need +3
        b["thoughts"][5]["example"] += " Экономь там где можно."
        # t7=687, need +13
        b["thoughts"][7]["example"] += " Большинство обид — про эго, а не про ситуацию."

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))

print("=== VERIFY samoraz_3b ===")
check_ids = {599, 600, 601, 602, 603, 605}
all_ok = True
for b in books:
    bid = b["id"]
    if bid not in check_ids:
        continue
    desc_len = len(b["description"])
    desc_ok = 125 <= desc_len <= 150
    issues = []
    if not desc_ok:
        issues.append("desc=%d" % desc_len)
    for i, t in enumerate(b["thoughts"]):
        total = len(t["title"]) + len(t["example"])
        if not (700 <= total <= 800):
            issues.append("t%d=%d" % (i, total))
    if issues:
        all_ok = False
        print("ID %d: %s" % (bid, " ".join(issues)))
if all_ok:
    print("ALL OK!")
