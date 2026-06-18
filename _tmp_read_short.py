import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

check_ids = [334, 335, 336, 470, 587, 588, 627, 632, 634]
for b in books:
    if b["id"] not in check_ids:
        continue
    for i, t in enumerate(b.get("thoughts", [])):
        s = len(t["title"]) + len(t["example"])
        if s < 700:
            need = 700 - s
            print(f"[{b['id']}][{i}] need+{need} ({s}): {t['title']}")
            print(f"  {t['example'][-120:]}")
            print()
