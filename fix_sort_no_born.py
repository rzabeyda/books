import json

# Manual order by importance
order = [
    # Мировые иконы
    178,  # Стив Джобс
    177,  # Билл Гейтс
    176,  # Марк Цукерберг
    175,  # Сергей Брин
    187,  # Джек Ма
    168,  # Никола Тесла
    169,  # Генри Форд
    170,  # Томас Эдисон
    184,  # Опра Уинфри
    180,  # Коко Шанель
    191,  # Фил Найт (Nike)
    192,  # Сэм Уолтон (Walmart)
    183,  # Ингвар Кампрад (IKEA)
    182,  # Говард Шульц (Starbucks)
    179,  # Харланд Сандерс (KFC)
    186,  # Дж. К. Роулинг
    181,  # Луи Вюиттон
    185,  # Ральф Лорен
    190,  # Эсте Лодер
    189,  # Ян Кум (WhatsApp)
    171,  # Александр Белл
    # Российский бизнес
    172,  # Павел Дуров
    188,  # Роман Абрамович
    215,  # Олег Тиньков
    173,  # Владимир Путин
    174,  # Сергей Мавроди
    # Блогеры и медиа
    203,  # Юрий Дудь
    199,  # Ксения Собчак
    207,  # Артемий Лебедев
    205,  # Илья Варламов
    193,  # Моргенштерн
    206,  # Wylsacom
    204,  # Амиран Сардаров
    194,  # Оля Бузова
    217,  # Гарик Харламов
    225,  # Павел Воля
    219,  # Little Big
    218,  # Влад А4
    214,  # Давидыч
    209,  # BadComedian
    213,  # Ивангай
    210,  # Николай Соболев
    212,  # Хованский
    208,  # Эльдар Джарахов
    222,  # Илья Соболев
    216,  # Азамат Мусагалиев
    223,  # Нурлан Сабуров
    224,  # Алексей Щербаков
    221,  # Сергей Орлов
    220,  # Эдвард Бил
    211,  # Антон Лапенко
    226,  # Мистер Макс
    # Женщины
    195,  # Оксана Самойлова
    196,  # Инстасамка
    198,  # Виктория Боня
    201,  # Алёна Водонаева
    200,  # Алёна Швец
    202,  # Вероника Степанова
    197,  # Олеся Иванченко
]

with open('/root/books/webapp/books.json') as f:
    books = json.load(f)

# Remove born from all books
for b in books:
    if 'born' in b:
        del b['born']

# Sort success stories by manual order
books_by_id = {b['id']: b for b in books}
other = [b for b in books if b.get('genre') != 'история успеха']
success_sorted = [books_by_id[i] for i in order if i in books_by_id]

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(other + success_sorted, f, ensure_ascii=False, indent=2)

print('Done. Success stories order:')
for i, b in enumerate(success_sorted, 1):
    print(f"  {i}. {b['title']}")
