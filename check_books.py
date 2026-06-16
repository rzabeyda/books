import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('books.json', encoding='utf-8') as f:
    books = json.load(f)
print('Total books:', len(books))
for b in books[-5:]:
    print(b.get('id'), '|', b.get('title'), '|', b.get('image'), '|', b.get('author'))
