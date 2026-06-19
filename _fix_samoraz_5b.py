import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

for b in books:
    bid = b["id"]

    if bid == 526:
        # t0=900, need trim ~100
        t = b["thoughts"][0]
        sep = t["example"].rfind("\n\n")
        if sep != -1:
            t["example"] = t["example"][:sep] + "\n\nАвторы проводили интервью с долгожителями Окинавы: никто из них не описывал своё предназначение как нечто грандиозное. Икигай — это конкретные ежедневные практики которые придают жизни смысл. Западная культура ищет «смысл жизни» — окинавская традиция находит смысл в жизни."

        # t1=808, need trim 8 — shorten last sentence
        t = b["thoughts"][1]
        old = "Окинавские долгожители не оптимизируют здоровье — они живут жизнью в которой здоровье возникает естественно."
        new = "Окинавские долгожители не оптимизируют здоровье — они живут жизнью где оно возникает само."
        if old in t["example"]:
            t["example"] = t["example"].replace(old, new)

        # t4=801, need trim 1+ — shorten middle phrase
        t = b["thoughts"][4]
        old = "метаанализа нескольких сотен исследований"
        new = "метаанализа сотен исследований"
        if old in t["example"]:
            t["example"] = t["example"].replace(old, new)

        # t8=807, need trim 7+ — shorten last sentence
        t = b["thoughts"][8]
        old = "Польза концепции не исчезает из-за того что перевод был несовершенен."
        new = "Польза концепции не исчезает от несовершенного перевода."
        if old in t["example"]:
            t["example"] = t["example"].replace(old, new)

    if bid == 528:
        # t0=820, need trim 20 — shorten last sentence
        t = b["thoughts"][0]
        old = "Если он просто занимает время не создавая ценности — он не заслуживает места в твоей жизни."
        new = "Если он не создаёт конкретной ценности — он не нужен."
        if old in t["example"]:
            t["example"] = t["example"].replace(old, new)

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))

print("=== VERIFY samoraz_5b ===")
check_ids = {526, 527, 528, 631}
all_ok = True
for b in books:
    bid = b["id"]
    if bid not in check_ids:
        continue
    desc_len = len(b["description"])
    issues = []
    if not (125 <= desc_len <= 150):
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
