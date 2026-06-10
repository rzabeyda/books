import json

# 203 Юрий Дудь, 205 Варламов, 206 Wylsacom, 204 Амиран, 208 Джарахов, 195 Самойлова, 202 Степанова
to_bloggers = {203, 204, 205, 206, 208, 195, 202}

books = json.load(open('/root/books/webapp/books.json'))

for b in books:
    if b['id'] in to_bloggers:
        print(f"блогеры: {b['title']}")
        b['genre'] = 'блогеры'

json.dump(books, open('/root/books/webapp/books.json', 'w'), ensure_ascii=False, indent=2)
print('done')
