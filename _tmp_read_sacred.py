import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

for b in books:
    if b.get("genre") != "священные писания":
        continue
    desc = b.get("description", "")
    print(f"\n=== [{b['id']}] ({len(desc)}) {b.get('title','')} ===")
    print(f"DESC: {desc}")
    for i, t in enumerate(b.get("thoughts", [])):
        total = len(t["title"]) + len(t["example"])
        print(f"[{i}] ({total}) {t['title']}")
        print(f"  {t['example']}")
