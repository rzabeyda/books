import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)
genres = {}
for b in books:
    g = b.get("genre", "")
    genres[g] = genres.get(g, 0) + 1
for g, cnt in sorted(genres.items(), key=lambda x: x[1]):
    print(f"  {cnt:3d}  {repr(g)}")
