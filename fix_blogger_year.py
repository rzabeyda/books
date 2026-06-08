import json

with open('/root/books/webapp/books.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

for book in books:
    if book.get('genre') == 'блогеры':
        book['year'] = None
        print(f"Убрана дата: {book['title']}")

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print('done')
