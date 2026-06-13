import json
books = json.load(open('/root/books/webapp/books.json', encoding='utf-8'))
for b in books:
    if b['id'] == 587:
        b['cover'] = 'top25_usa_products.png'
    if b['id'] == 588:
        b['cover'] = '10_rules_real_life.png'
with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False)
print('done')
