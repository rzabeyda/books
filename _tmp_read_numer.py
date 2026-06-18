import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

for b in books:
    if b.get("genre") != "нумерология":
        continue
    print(f"\n=== [{b['id']}] {b.get('title','')} ===")
    for i, t in enumerate(b.get("thoughts", [])):
        total = len(t["title"]) + len(t["example"])
        print(f"[{i}] ({total}) {t['title']}")
        print(f"  {t['example']}")
