import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)
bad_books = []
for b in books:
    bad = 0
    for t in b.get("thoughts", []):
        if t["example"].count("?") > 5:
            bad += 1
    if bad > 0:
        bad_books.append((b["id"], b.get("title","")[:30], bad, len(b.get("thoughts",[]))))
print(f"Books with corrupted thoughts: {len(bad_books)}")
for bid, title, bad, total in bad_books:
    print(f"  [{bid}] {title}: {bad}/{total} corrupted")
