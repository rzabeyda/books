import json

with open('/root/books/webapp/books.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

for b in books:
    if b.get('id') == 165:
        print(f"Было: {b['cover']}")
        b['cover'] = 'leiden.jpg'
        print(f"Стало: {b['cover']}")

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)
