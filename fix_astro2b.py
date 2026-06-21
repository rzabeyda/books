import json

fixes = {
    698: { 7: " Это простая и важная идея." },
    699: { 0: " Это уважительная позиция." }
}

def trim(title, example, mx=800):
    if len(title) + len(example) <= mx:
        return example
    budget = mx - len(title)
    chunk = example[:budget]
    last = max(chunk.rfind("."), chunk.rfind("!"), chunk.rfind("?"))
    return example[:last+1] if last > 0 else example[:budget]

with open("C:/books/astro_batch2.json", encoding="utf-8") as f:
    books = json.load(f)

for b in books:
    bid = b["id"]
    if bid not in fixes:
        continue
    for i, t in enumerate(b["thoughts"]):
        if i in fixes[bid]:
            t["example"] += fixes[bid][i]
            t["example"] = trim(t["title"], t["example"])

with open("C:/books/astro_batch2.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False)

all_ok = True
for b in books:
    desc_len = len(b["description"])
    issues = []
    if not (125 <= desc_len <= 150):
        issues.append(f"desc={desc_len}")
    for i, t in enumerate(b["thoughts"]):
        total = len(t["title"]) + len(t["example"])
        if not (700 <= total <= 800):
            issues.append(f"t{i}={total}")
            all_ok = False
    print(f"  {b['id']} {b['title'][:40]}: desc={desc_len} " + (", ".join(issues) if issues else "OK"))
print("All OK" if all_ok else "ISSUES FOUND")
