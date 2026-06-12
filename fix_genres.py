import json

with open('/root/books/webapp/books.json', encoding='utf-8') as f:
    books = json.load(f)

moves = {
    342: 'фантастика',   # Дюна: сказки → фантастика
    479: 'фантастика',   # Автостопом по галактике: сказки → фантастика
    482: 'фантастика',   # Гиперион: сказки → фантастика
    481: 'фантастика',   # Тёмная башня: сказки → фантастика
    494: 'фантастика',   # Цветы для Элджернона: художественная → фантастика
    574: 'классика',     # Зулейха: детективы → классика
    227: 'сказки',       # Четвёртое крыло: фантастика → сказки
    259: 'сказки',       # Сумерки: фантастика → сказки
}

for b in books:
    if b['id'] in moves:
        old = b['genre']
        b['genre'] = moves[b['id']]
        print(f"ID {b['id']}: {b['title']} | {old} → {b['genre']}")

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

print("Done.")
