import json
books = json.load(open('/root/books/webapp/books.json', encoding='utf-8'))
changed = 0
for b in books:
    if b.get('author', '') == 'Роман Забейда':
        b['genre'] = 'от автора'
        changed += 1
        print(b['id'], b['title'])
with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False)
print('Changed:', changed)
