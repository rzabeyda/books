import json
books = json.load(open('/root/books/webapp/books.json'))
for b in books:
    if b['id'] == 153:
        b['platform'] = 'Twitch'
        print(f"updated: {b['title']} — {b['platform']}")
json.dump(books, open('/root/books/webapp/books.json', 'w'), ensure_ascii=False, indent=2)
print('done')
