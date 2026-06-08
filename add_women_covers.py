import json

with open('/root/books/webapp/books.json', encoding='utf-8') as f:
    books = json.load(f)

new_people = [
    {"title": "Ольга Бузова",       "author": "Телеведущая, певица",  "cover": "buzova_olya.jpg"},
    {"title": "Оксана Самойлова",   "author": "Блогер, предприниматель", "cover": "samoilova_oksana.jpg"},
    {"title": "Инстасамка",         "author": "Рэпер, блогер",        "cover": "instasamka.jpg"},
    {"title": "Олеся Иванченко",    "author": "Блогер",               "cover": "ivan4enko_olesja.jpg"},
    {"title": "Виктория Боня",      "author": "Телеведущая, блогер",  "cover": "bonya_vika.jpg"},
    {"title": "Ксения Собчак",      "author": "Журналист, телеведущая","cover": "sob4ak_ksenia.jpg"},
    {"title": "Алена Швец",         "author": "Певица",               "cover": "shvec_alena.jpg"},
    {"title": "Алеся Водонаева",    "author": "Телеведущая, блогер",  "cover": "vodonajeva_alena.jpg"},
]

max_id = max(b['id'] for b in books)
added = 0
for p in new_people:
    if any(b['title'] == p['title'] and b['genre'] == 'история успеха' for b in books):
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
    print(f"добавлен: {p['title']} → id {max_id}")
    added += 1

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print(f'\nДобавлено: {added}. Всего: {len(books)}')
