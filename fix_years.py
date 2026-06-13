import json
books = json.load(open('/root/books/webapp/books.json', encoding='utf-8'))
fix = {470: 2026, 471: 2026}
for b in books:
    if b['id'] in fix:
        b['year'] = fix[b['id']]
with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False)
print('done')
