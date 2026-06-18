import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

for b in books:
    desc = b.get("description", "")
    if len(desc) > 150:
        print(f"[{b['id']}] ({len(desc)}) {b.get('genre','')} | {b.get('title','')[:35]}")
        print(f"  {desc}")
        print()
