import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)
for b in books:
    if b["id"] != 598:
        continue
    for i, t in enumerate(b.get("thoughts", [])):
        if i in [19, 37]:
            total = len(t["title"]) + len(t["example"])
            print(f"[{i}] {total}: {t['title']}")
            print(f"  example end: {repr(t['example'][-120:])}")
