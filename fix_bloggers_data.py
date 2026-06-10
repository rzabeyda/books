import json

# platform: YouTube / TikTok
# subs_label: отображаемое кол-во подписчиков
blogger_data = {
    149: {'platform': 'YouTube', 'subs_label': '1.5 млн подписчиков'},   # Антон Петряков
    150: {'platform': 'YouTube', 'subs_label': '11 млн подписчиков'},    # Моргенштерн
    151: {'platform': 'YouTube', 'subs_label': '3 млн подписчиков'},     # Геннадий М
    152: {'platform': 'YouTube', 'subs_label': '2 млн подписчиков'},     # Максим Воронович
    153: {'platform': 'YouTube', 'subs_label': '6 млн подписчиков'},     # Мэлстрой
    154: {'platform': 'YouTube', 'subs_label': '3 млн подписчиков'},     # Вероника Степанова
    203: {'platform': 'YouTube', 'subs_label': '10 млн подписчиков'},    # Юрий Дудь
    204: {'platform': 'YouTube', 'subs_label': '3 млн подписчиков'},     # Амиран Сардаров
    205: {'platform': 'YouTube', 'subs_label': '2 млн подписчиков'},     # Илья Варламов
    206: {'platform': 'YouTube', 'subs_label': '10 млн подписчиков'},    # Wylsacom
    208: {'platform': 'YouTube', 'subs_label': '4 млн подписчиков'},     # Эльдар Джарахов
    209: {'platform': 'YouTube', 'subs_label': '4 млн подписчиков'},     # BadComedian
    210: {'platform': 'YouTube', 'subs_label': '7 млн подписчиков'},     # Николай Соболев
    212: {'platform': 'YouTube', 'subs_label': '5 млн подписчиков'},     # Хованский
    213: {'platform': 'YouTube', 'subs_label': '10 млн подписчиков'},    # Ивангай
    214: {'platform': 'YouTube', 'subs_label': '2 млн подписчиков'},     # Давидыч
    218: {'platform': 'YouTube', 'subs_label': '50 млн подписчиков'},    # Влад А4
    220: {'platform': 'YouTube', 'subs_label': '2 млн подписчиков'},     # Эдвард Бил
    226: {'platform': 'YouTube', 'subs_label': '25 млн подписчиков'},    # Мистер Макс
    195: {'platform': 'YouTube', 'subs_label': '5 млн подписчиков'},     # Оксана Самойлова
    202: {'platform': 'YouTube', 'subs_label': '3 млн подписчиков'},     # Вероника Степанова
}

books = json.load(open('/root/books/webapp/books.json'))

for b in books:
    # Move Илья Соболев back
    if b['id'] == 222:
        b['genre'] = 'история успеха'
        print(f"история успеха: {b['title']}")
    # Add platform/subs to bloggers
    if b['id'] in blogger_data:
        b.update(blogger_data[b['id']])
        print(f"updated: {b['title']} — {b['platform']} — {b['subs_label']}")

json.dump(books, open('/root/books/webapp/books.json', 'w'), ensure_ascii=False, indent=2)
print('done')
