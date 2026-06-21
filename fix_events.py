import json

def trim(title, example, mx=800):
    if len(title) + len(example) <= mx:
        return example
    budget = mx - len(title)
    chunk = example[:budget]
    last = max(chunk.rfind('.'), chunk.rfind('!'), chunk.rfind('?'))
    return example[:last+1] if last > 0 else example[:budget]

with open("C:/books/events_batch.json", encoding="utf-8") as f:
    books = json.load(f)

for b in books:
    bid = b["id"]

    # Fix descriptions
    if bid == 735:
        b["description"] = "Шесть лет войны охватили весь мир. 70 миллионов погибших, атомная бомба, Холокост и совершенно новый мировой порядок из пепла."
    elif bid == 738:
        b["description"] = "19 вооружённых террористов угнали четыре самолёта и атаковали Америку. 3000 погибших и двадцать лет войн, изменивших мир навсегда."
    elif bid == 740:
        b["description"] = "Крах фондового рынка в 1929 году запустил экономическую катастрофу охватившую весь мир. Безработица, голод и политический радикализм изменили XX век."

    # Fix thought 737 t6 (too short, 594)
    if bid == 737:
        t = b["thoughts"][6]
        # Add "совершенно" to make it longer
        t["example"] = t["example"].replace(
            "скорее всего обесцвечены солнечной радиацией и стоят белыми.",
            "скорее всего обесцвечены солнечной радиацией и стоят совершенно белыми."
        )

    # Fix thought 739 t1 (too long, 819)
    if bid == 739:
        t = b["thoughts"][1]
        t["example"] = t["example"].replace(
            "Гласность — открытость — должна",
            "Гласность должна"
        ).replace(
            "В России многие — предателем.",
            "В России — предателем."
        )

    # Fix thoughts 741 t3 and 742 t3 (slightly too long)
    if bid == 741:
        t = b["thoughts"][3]
        t["example"] = trim(t["title"], t["example"])
    if bid == 742:
        t = b["thoughts"][3]
        t["example"] = trim(t["title"], t["example"])

with open("C:/books/events_batch.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False)

# Validate
all_ok = True
for b in books:
    d = len(b["description"])
    issues = []
    if not (125 <= d <= 150): issues.append(f"desc={d}")
    for i, t in enumerate(b["thoughts"]):
        total = len(t["title"]) + len(t["example"])
        if not (600 <= total <= 800):
            issues.append(f"t{i}={total}")
            all_ok = False
    status = ", ".join(issues) if issues else "OK"
    print(f"  {b['id']} {b['title'][:20]}: desc={d} {status}")
print("All OK!" if all_ok else "ISSUES REMAIN")
