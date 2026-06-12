import json

with open('/root/books/webapp/books.json', encoding='utf-8') as f:
    books = json.load(f)

esoterica_ids = {294, 93, 31, 27, 112, 94, 95}

for b in books:
    if b['id'] in esoterica_ids:
        b['genre'] = 'саморазвитие'
        print(f"  {b['id']}: {b['title']} -> саморазвитие")

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

print("Saved.")
