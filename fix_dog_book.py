import json

with open('/root/books/webapp/books.json', encoding='utf-8') as f:
    books = json.load(f)

for b in books:
    if b['id'] == 9:
        print(f"Было: {b['genre']} | {b['title']}")
        b['genre'] = 'психология'
        print(f"Стало: {b['genre']}")

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)
