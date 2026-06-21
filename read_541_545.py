import json
with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

ids = [541, 542, 543, 544, 545]
for book in data:
    if book['id'] in ids:
        dlens = len(book['description'])
        print(f'ID={book["id"]:3d} {book["title"][:22]:22s}: desc={dlens}')
        for i, t in enumerate(book['thoughts']):
            has_life = 'life' in t
            print(f'  T{i} [{len(t["example"])}] life={has_life} {t["title"][:35]}')
