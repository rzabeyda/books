import json

with open('/root/books/webapp/books.json') as f:
    books = json.load(f)

updated = 0
for b in books:
    if 'world_reads_label' in b and '+' in b['world_reads_label']:
        b['world_reads_label'] = b['world_reads_label'].replace('+', '')
        updated += 1
        print(b['title'], '->', b['world_reads_label'])

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print('Done:', updated)
