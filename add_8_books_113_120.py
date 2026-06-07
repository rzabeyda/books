
import json

with open('/root/books/webapp/books.json', 'r') as f:
    books = json.load(f)

new_books = [
    {
        "id": 113,
        "title": "Разбуди в себе великана",
        "author": "Тони Роббинс",
        "cover": "covers/razbudi_v_sebje_velikana.jpg",
        "world_reads": 10000000,
        "world_reads_label": "Тираж 10млн+",
        "year": 1991,
        "genre": "саморазвитие",
        "thoughts": []
    },
    {
        "id": 114,
        "title": "Новая психология успеха",
        "author": "Кэрол Дуэк",
        "cover": "covers/novaya_psihologiya_uspeha.jpg",
        "world_reads": 5000000,
        "world_reads_label": "Тираж 5млн+",
        "year": 2006,
        "genre": "психология",
        "thoughts": []
    },
    {
        "id": 115,
        "title": "Думай как миллионер",
        "author": "Т. Харв Экер",
        "cover": "covers/dumay_kak_millioner.png",
        "world_reads": 5000000,
        "world_reads_label": "Тираж 5млн+",
        "year": 2005,
        "genre": "бизнес",
        "thoughts": []
    },
    {
        "id": 116,
        "title": "Как привести дела в порядок",
        "author": "Дэвид Аллен",
        "cover": "covers/kak_privesti_dela_v_porjadok.jpg",
        "world_reads": 2000000,
        "world_reads_label": "Тираж 2млн+",
        "year": 2001,
        "genre": "саморазвитие",
        "thoughts": []
    },
    {
        "id": 117,
        "title": "На пределе",
        "author": "Эрик Бертран Ларссен",
        "cover": "covers/na_predele.jpg",
        "world_reads": 1000000,
        "world_reads_label": "Тираж 1млн+",
        "year": 2012,
        "genre": "саморазвитие",
        "thoughts": []
    },
    {
        "id": 118,
        "title": "Магия утра",
        "author": "Хэл Элрод",
        "cover": "covers/magiya_utra.jpg",
        "world_reads": 5000000,
        "world_reads_label": "Тираж 5млн+",
        "year": 2012,
        "genre": "саморазвитие",
        "thoughts": []
    },
    {
        "id": 119,
        "title": "Съешьте лягушку!",
        "author": "Брайан Трейси",
        "cover": "covers/sjewte_ljaguwku.jpg",
        "world_reads": 3000000,
        "world_reads_label": "Тираж 3млн+",
        "year": 2001,
        "genre": "саморазвитие",
        "thoughts": []
    },
    {
        "id": 120,
        "title": "Глубокая работа",
        "author": "Кэл Ньюпорт",
        "cover": "covers/glubokaya_rabota.jpg",
        "world_reads": 1000000,
        "world_reads_label": "Тираж 1млн+",
        "year": 2016,
        "genre": "саморазвитие",
        "thoughts": []
    },
]

existing_ids = {b['id'] for b in books}
added = 0
for nb in new_books:
    if nb['id'] not in existing_ids:
        books.append(nb)
        print(f"ID {nb['id']}: {nb['title']} ({nb['author']}) — добавлен")
        added += 1
    else:
        print(f"ID {nb['id']}: уже существует, пропущен")

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

print(f'Добавлено: {added}. Итого книг: {len(books)}. Done.')
