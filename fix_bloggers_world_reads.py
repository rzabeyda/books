import json

books = json.load(open('/root/books/webapp/books.json'))

for b in books:
    if b['genre'] in ('блогеры', 'стримеры'):
        b['world_reads'] = 0
        b['world_reads_label'] = ''

json.dump(books, open('/root/books/webapp/books.json', 'w'), ensure_ascii=False, indent=2)
print('done')
