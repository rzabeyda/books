import json

with open('/root/books/webapp/books.json', encoding='utf-8') as f:
    books = json.load(f)

max_id = max(b['id'] for b in books)

new_people = [
    {"title": "Харланд Сандерс", "author": "KFC", "cover": "sanders.jpg"},
    {"title": "Коко Шанель",     "author": "Chanel", "cover": "chanel.jpg"},
    {"title": "Луи Вюиттон",     "author": "Louis Vuitton", "cover": "vuitton.jpg"},
    {"title": "Говард Шульц",    "author": "Starbucks", "cover": "schultz.jpg"},
    {"title": "Ингвар Кампрад",  "author": "IKEA", "cover": "kamprad.jpg"},
    {"title": "Опра Уинфри",     "author": "OWN", "cover": "oprah.jpg"},
    {"title": "Ральф Лорен",     "author": "Ralph Lauren", "cover": "lauren.jpg"},
    {"title": "Дж. К. Роулинг", "author": "Harry Potter", "cover": "rowling.jpg"},
    {"title": "Джек Ма",         "author": "Alibaba", "cover": "jackma.jpg"},
    {"title": "Роман Абрамович", "author": "Chelsea FC", "cover": "abramovich.jpg"},
    {"title": "Ян Кум",          "author": "WhatsApp", "cover": "koum.jpg"},
    {"title": "Эсте Лодер",      "author": "Estée Lauder", "cover": "lauder.jpg"},
    {"title": "Фил Найт",        "author": "Nike", "cover": "knight.jpg"},
    {"title": "Сэм Уолтон",      "author": "Walmart", "cover": "walton.jpg"},
]

added = 0
for p in new_people:
    if any(b['title'] == p['title'] for b in books):
        print('пропуск (уже есть):', p['title'])
        continue
    max_id += 1
    books.append({
        "id": max_id,
        "title": p['title'],
        "author": p['author'],
        "genre": "история успеха",
        "cover": p['cover'],
        "year": 0,
        "world_reads": 0,
        "world_reads_label": "",
        "description": "",
        "thoughts": []
    })
    print('добавлен:', p['title'], '→ id', max_id)
    added += 1

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print(f'\nДобавлено: {added}. Всего книг: {len(books)}')
