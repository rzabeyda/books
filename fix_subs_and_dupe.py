import json

books = json.load(open('/root/books/webapp/books.json'))

# Remove duplicate Степанова (id=202)
books = [b for b in books if b['id'] != 202]

# Fix subscriber counts
fixes = {
    149: '950 тыс. подписчиков',
    151: '250 тыс. подписчиков',
    152: '60 тыс. подписчиков',
}

for b in books:
    if b['id'] in fixes:
        b['subs_label'] = fixes[b['id']]
        print(f"updated: {b['title']} — {b['subs_label']}")

print('removed: Вероника Степанова id=202')

json.dump(books, open('/root/books/webapp/books.json', 'w'), ensure_ascii=False, indent=2)
print('done')
