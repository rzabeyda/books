import json

with open('/root/books/webapp/books.json', 'r') as f:
    books = json.load(f)

new_books = [
    {"id": 97,  "title": "1776",                                          "author": "Дэвид Маккаллоу",       "genre": "история",  "cover": "1776_david.jpg",                          "thoughts": []},
    {"id": 98,  "title": "Августовские пушки",                            "author": "Барбара Такман",         "genre": "история",  "cover": "avgustovskie_puwki.jpg",                  "thoughts": []},
    {"id": 99,  "title": "Запасной",                                      "author": "Принц Гарри",            "genre": "мемуары",  "cover": "bez_poter_princ.jpg",                     "thoughts": []},
    {"id": 100, "title": "Конец истории и последний человек",             "author": "Фрэнсис Фукуяма",        "genre": "политика", "cover": "konec_istorii_I_poslednij_4elovek.jpg",   "thoughts": []},
    {"id": 101, "title": "Есть, молиться, любить",                        "author": "Элизабет Гилберт",       "genre": "мемуары",  "cover": "est_molitsa_ljubit.jpg",                  "thoughts": []},
    {"id": 102, "title": "Краткая история времени",                       "author": "Стивен Хокинг",          "genre": "nonfiction","cover": "kratkaya_istoriya_vremeni.jpg",            "thoughts": []},
    {"id": 103, "title": "Я знаю, почему птица в клетке поёт",           "author": "Майя Энджелоу",          "genre": "мемуары",  "cover": "ya_znaju_po4emy_ptica_v_kletke_pojit.jpg","thoughts": []},
    {"id": 104, "title": "Homo Deus: Краткая история будущего",           "author": "Юваль Ной Харари",       "genre": "nonfiction","cover": "kratkaya_istoriya_buduwego.jpg",           "thoughts": []},
    {"id": 105, "title": "Цивилизация. Чем Запад отличается от остального мира", "author": "Найл Фергюсон", "genre": "история",  "cover": "civilizaciya_4em_zapad_otli4aeca.jpg",    "thoughts": []},
    {"id": 106, "title": "Ночь",                                          "author": "Эли Визель",             "genre": "мемуары",  "cover": "no4_vizel.jpg",                           "thoughts": []},
    {"id": 107, "title": "Образование",                                   "author": "Тара Вествовер",         "genre": "мемуары",  "cover": "obrazovanie_tara.jpg",                    "thoughts": []},
    {"id": 108, "title": "Прах Анжелы",                                   "author": "Фрэнк Маккорт",          "genre": "мемуары",  "cover": "prah_anzhely.jpg",                        "thoughts": []},
    {"id": 109, "title": "Ружья, микробы и сталь",                        "author": "Джаред Даймонд",         "genre": "история",  "cover": "ruzya_mikroby_i_stal.jpg",                "thoughts": []},
    {"id": 110, "title": "Взлёт и падение Третьего рейха",                "author": "Уильям Ширер",           "genre": "история",  "cover": "vljot_i_padenie_3_reiha.jpg",             "thoughts": []},
    {"id": 111, "title": "Становление",                                   "author": "Мишель Обама",           "genre": "мемуары",  "cover": "stanovlenie.jpg",                         "thoughts": []},
]

existing_ids = {b['id'] for b in books}
added = 0
for nb in new_books:
    if nb['id'] not in existing_ids:
        books.append(nb)
        print(f"ID {nb['id']}: {nb['title']} [{nb['genre']}]")
        added += 1
    else:
        print(f"SKIP ID {nb['id']}: already exists")

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

print(f'\nДобавлено: {added}. Всего книг: {len(books)}')
