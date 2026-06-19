import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

def trim_to_fit(title, example, max_total=800):
    total = len(title) + len(example)
    if total <= max_total:
        return example
    max_ex = max_total - len(title)
    chunk = example[:max_ex]
    for sep in [". ", "! ", "? "]:
        pos = chunk.rfind(sep)
        if pos > max_ex - 200:
            return chunk[:pos+1]
    pos = chunk.rfind(" ")
    return chunk[:pos] + "."

trim_ids = {4, 9, 13, 14, 15, 16, 21, 22, 45, 46, 47, 48}

for b in books:
    if b["id"] not in trim_ids:
        continue
    for t in b.get("thoughts", []):
        total = len(t["title"]) + len(t["example"])
        if total > 800:
            t["example"] = trim_to_fit(t["title"], t["example"])

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))

print("=== VERIFY psych_1 (trim >800) ===")
all_ok = True
for b in books:
    if b["id"] not in trim_ids:
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
