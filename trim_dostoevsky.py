import json

def trim(title, example, mx=800):
    if len(title) + len(example) <= mx:
        return example
    budget = mx - len(title)
    chunk = example[:budget]
    last = max(chunk.rfind("."), chunk.rfind("!"), chunk.rfind("?"))
    return example[:last+1] if last > 0 else example[:budget]

with open("C:/books/dostoevsky_books.json", encoding="utf-8") as f:
    books = json.load(f)

all_ok = True
for b in books:
    for i, t in enumerate(b["thoughts"]):
        t["example"] = trim(t["title"], t["example"])

with open("C:/books/dostoevsky_books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False)

print("После trim:")
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
    print(f"  {b['id']} {b['title']}: desc={desc_len} " + (", ".join(issues) if issues else "OK"))
print("All OK" if all_ok else "ISSUES FOUND")
