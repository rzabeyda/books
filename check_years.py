import json
books = json.load(open('/root/books/webapp/books.json', encoding='utf-8'))
for b in books:
    if b.get('genre') == 'от автора':
        print(b['id'], b.get('year'), b['title'])
