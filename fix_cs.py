import json

def trim(title, example, mx=800):
    if len(title) + len(example) <= mx:
        return example
    budget = mx - len(title)
    chunk = example[:budget]
    last = max(chunk.rfind('.'), chunk.rfind('!'), chunk.rfind('?'))
    return example[:last+1] if last > 0 else example[:budget]

with open("C:/books/cs_batch.json", encoding="utf-8") as f:
    books = json.load(f)

for b in books:
    for i in [0, 4, 7, 8, 9]:
        t = b["thoughts"][i]
        t["example"] = trim(t["title"], t["example"])

with open("C:/books/cs_batch.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False)

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
    print(f"  {b['id']}: desc={d} {status}")
print("All OK!" if all_ok else "ISSUES REMAIN")
