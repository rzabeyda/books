import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

genres = ["нумерология", "отношения", "от автора"]
for b in books:
    if b.get("genre") not in genres:
        continue
    desc = b.get("description", "")
    print(f"[{b['id']}] ({len(desc)}) {b.get('title','')[:40]}")
    print(f"  {desc}")
    print()
