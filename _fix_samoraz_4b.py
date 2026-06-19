import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

for b in books:
    if b["id"] != 123:
        continue
    # t0=823, need to trim 23+ chars from end
    t0 = b["thoughts"][0]
    old_end = "вместо размытия между двадцатью посредственными результатами."
    new_end = "вместо посредственности в многом."
    if t0["example"].endswith(old_end):
        t0["example"] = t0["example"][:-len(old_end)] + new_end
    # t2=688, need +12 min
    b["thoughts"][2]["example"] += " Эссенциализм — это про выбор а не про объём."

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))

print("=== VERIFY samoraz_4b (ID 123) ===")
all_ok = True
for b in books:
    if b["id"] != 123:
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
        print("ID 123: %s" % " ".join(issues))
if all_ok:
    print("ALL OK!")
