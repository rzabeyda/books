import json

new_books = [
    {"id": 203, "title": "Юрий Дудь", "author": "Юрий Дудь", "cover": "dud.jpg"},
    {"id": 204, "title": "Амиран Сардаров", "author": "Амиран Сардаров", "cover": "sardarov.jpg"},
    {"id": 205, "title": "Илья Варламов", "author": "Илья Варламов", "cover": "varlamov.jpg"},
    {"id": 206, "title": "Wylsacom", "author": "Wylsacom", "cover": "wylsacom.jpg"},
    {"id": 207, "title": "Артемий Лебедев", "author": "Артемий Лебедев", "cover": "lebedev.jpg"},
    {"id": 208, "title": "Эльдар Джарахов", "author": "Эльдар Джарахов", "cover": "dzarakhov.jpg"},
    {"id": 209, "title": "BadComedian", "author": "BadComedian", "cover": "badcomedian.jpg"},
    {"id": 210, "title": "Николай Соболев", "author": "Николай Соболев", "cover": "sobolev_n.jpg"},
    {"id": 211, "title": "Антон Лапенко", "author": "Антон Лапенко", "cover": "lapenko.jpg"},
    {"id": 212, "title": "Хованский", "author": "Хованский", "cover": "khovansky.jpg"},
    {"id": 213, "title": "Ивангай", "author": "Ивангай", "cover": "ivangay.jpg"},
    {"id": 214, "title": "Давидыч", "author": "Давидыч", "cover": "davidych.jpg"},
    {"id": 215, "title": "Олег Тиньков", "author": "Олег Тиньков", "cover": "tinkov.jpg"},
    {"id": 216, "title": "Азамат Мусагалиев", "author": "Азамат Мусагалиев", "cover": "musagaliev.jpg"},
    {"id": 217, "title": "Гарик Харламов", "author": "Гарик Харламов", "cover": "kharlamov.jpg"},
    {"id": 218, "title": "Влад А4", "author": "Влад А4", "cover": "vlad_a4.jpg"},
    {"id": 219, "title": "Little Big", "author": "Little Big", "cover": "little_big.jpg"},
    {"id": 220, "title": "Эдвард Бил", "author": "Эдвард Бил", "cover": "beal.jpg"},
    {"id": 221, "title": "Сергей Орлов", "author": "Сергей Орлов", "cover": "orlov_s.jpg"},
    {"id": 222, "title": "Илья Соболев", "author": "Илья Соболев", "cover": "sobolev_i.jpg"},
    {"id": 223, "title": "Нурлан Сабуров", "author": "Нурлан Сабуров", "cover": "saburov.jpg"},
    {"id": 224, "title": "Алексей Щербаков", "author": "Алексей Щербаков", "cover": "shcherbakov.jpg"},
    {"id": 225, "title": "Павел Воля", "author": "Павел Воля", "cover": "volya.jpg"},
    {"id": 226, "title": "Мистер Макс", "author": "Мистер Макс", "cover": "mister_max.jpg"},
]

with open('/root/books/webapp/books.json') as f:
    books = json.load(f)

for nb in new_books:
    books.append({
        "id": nb["id"],
        "title": nb["title"],
        "author": nb["author"],
        "cover": nb["cover"],
        "genre": "история успеха",
        "world_reads": 0,
        "world_reads_label": "",
        "description": "",
        "thoughts": []
    })
    print('Added: ' + nb["title"] + ' id=' + str(nb["id"]))

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print('Done. Total books: ' + str(len(books)))
