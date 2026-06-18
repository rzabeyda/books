import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

need_ids = [127, 229, 242, 243, 244, 245, 246, 247, 532, 534]
for b in books:
    if b["id"] not in need_ids:
        continue
    print(f"\n=== [{b['id']}] {b.get('title','')} ===")
    for i, t in enumerate(b.get("thoughts", [])):
        total = len(t["title"]) + len(t["example"])
        print(f"[{i}] ({total}) {t['title']}")
        print(f"  {t['example']}")
