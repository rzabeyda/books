import json

with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

removed = 0
for book in data:
    for thought in book.get('thoughts', []):
        if 'question' in thought:
            del thought['question']
            removed += 1

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Удалено question из {removed} мыслей')
