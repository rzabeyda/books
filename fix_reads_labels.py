import json, re

books = json.load(open('/root/books/webapp/books.json'))

fixed = 0
for b in books:
    label = b.get('world_reads_label', '')
    if label:
        new_label = re.sub(r'(\d)(млн|тыс)', r'\1 \2', label)
        if new_label != label:
            b['world_reads_label'] = new_label
            fixed += 1

json.dump(books, open('/root/books/webapp/books.json', 'w'), ensure_ascii=False, indent=2)
print(f'Fixed {fixed} labels')
