import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)
for b in books:
    g = b.get("genre", "")
    # print genre as hex to avoid encoding issues
    if any(c in g for c in ["о","т"," "]):
        words = g.split()
        if len(words) == 2 and len(words[0]) == 2 and len(words[1]) == 6:
            print(f"ID={b['id']} genre_hex={g.encode('utf-8').hex()}")
