import json, sys
sys.stdout.reconfigure(encoding='utf-8')
books = json.load(open('/root/books/books.json'))
print('Total:', len(books))
for b in books[-5:]:
    print(b.get('id'), '|', b.get('title'), '|', b.get('image'), '|', b.get('author'))
