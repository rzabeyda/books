import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)
for b in books:
    if b["id"] not in [334, 335]:
        continue
    for i, t in enumerate(b.get("thoughts", [])):
        s = len(t["title"]) + len(t["example"])
        if s < 700:
            print(f"[{b['id']}][{i}] total={s} need+{700-s}: {t['title']}")
            print(f"  {t['example'][-150:]}")
