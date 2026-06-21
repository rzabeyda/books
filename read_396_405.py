import json
with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

ids = list(range(396, 406))
for book in data:
    if book['id'] in ids:
        dlens = len(book['description'])
        print(f'ID={book["id"]:3d} {book["title"][:22]:22s}: desc={dlens}')
        for i, t in enumerate(book['thoughts']):
            print(f'  T{i} [{len(t["example"])}] {t["title"][:40]}')
