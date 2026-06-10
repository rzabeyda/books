import json

# Move to блогеры by id
to_bloggers = {209, 210, 212, 213, 214, 218, 220, 222, 226}
# 209 BadComedian, 210 Николай Соболев, 212 Хованский, 213 Ивангай
# 214 Давидыч, 218 Влад А4, 220 Эдвард Бил, 222 Илья Соболев, 226 Мистер Макс

# Move to отношения by id
to_relations = {229, 230}
# 229 Всё о любви, 230 Нормальные люди

books = json.load(open('/root/books/webapp/books.json'))

for b in books:
    if b['id'] in to_bloggers:
        print(f"блогеры: {b['title']}")
        b['genre'] = 'блогеры'
    elif b['id'] in to_relations:
        print(f"отношения: {b['title']}")
        b['genre'] = 'отношения'

json.dump(books, open('/root/books/webapp/books.json', 'w'), ensure_ascii=False, indent=2)
print('done')
