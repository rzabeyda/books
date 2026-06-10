import json

with open('/root/books/webapp/books.json', 'r') as f:
    data = json.load(f)

max_id = max(b['id'] for b in data)

new_books = [
    {"id": max_id+1, "title": "Дама с собачкой", "author": "Антон Чехов", "cover": "lady_with_the_dog.jpg", "world_reads": 5000000, "world_reads_label": "Тираж 5 млн", "genre": "классика", "year": 1899, "description": "Лирическая повесть о запретной любви, одиночестве и невозможности счастья — одна из лучших новелл мировой литературы.", "thoughts": []},
    {"id": max_id+2, "title": "Вишнёвый сад", "author": "Антон Чехов", "cover": "Cherry_orchard.jpg", "world_reads": 4000000, "world_reads_label": "Тираж 4 млн", "genre": "классика", "year": 1904, "description": "Последняя пьеса Чехова — о гибели дворянского уклада, неспособности принять перемены и ускользающем прошлом.", "thoughts": []},
    {"id": max_id+3, "title": "Палата №6", "author": "Антон Чехов", "cover": "ward_no_6.jpg", "world_reads": 3000000, "world_reads_label": "Тираж 3 млн", "genre": "классика", "year": 1892, "description": "Повесть о враче психиатрической больницы, который сам оказывается за решёткой — жёсткая метафора общества и власти.", "thoughts": []},
    {"id": max_id+4, "title": "Собор Парижской Богоматери", "author": "Виктор Гюго", "cover": "hunchback_of_notre_dame.jpg", "world_reads": 10000000, "world_reads_label": "Тираж 10 млн", "genre": "классика", "year": 1831, "description": "Трагедия горбуна Квазимодо и прекрасной Эсмеральды на фоне средневекового Парижа — гимн красоте, уродству и состраданию.", "thoughts": []},
    {"id": max_id+5, "title": "Человек, который смеётся", "author": "Виктор Гюго", "cover": "man_who_laughs.jpg", "world_reads": 2000000, "world_reads_label": "Тираж 2 млн", "genre": "классика", "year": 1869, "description": "История обезображенного аристократа, чья вечная улыбка скрывает боль — роман о несправедливости, маске и истинном благородстве.", "thoughts": []},
    {"id": max_id+6, "title": "Превращение", "author": "Франц Кафка", "cover": "metamorphosis.jpg", "world_reads": 8000000, "world_reads_label": "Тираж 8 млн", "genre": "классика", "year": 1915, "description": "Коммивояжёр просыпается насекомым. Абсурдная притча об отчуждении, семье и том, что делает нас людьми.", "thoughts": []},
    {"id": max_id+7, "title": "Замок", "author": "Франц Кафка", "cover": "the_castle.jpg", "world_reads": 3000000, "world_reads_label": "Тираж 3 млн", "genre": "классика", "year": 1926, "description": "Землемер К. пытается попасть в Замок — и не может. Роман-лабиринт о бюрократии, власти и бессилии человека перед системой.", "thoughts": []},
    {"id": max_id+8, "title": "Памяти Каталонии", "author": "Джордж Оруэлл", "cover": "homage_to_catalonia.jpg", "world_reads": 1000000, "world_reads_label": "Тираж 1 млн", "genre": "классика", "year": 1938, "description": "Личный репортаж Оруэлла с Гражданской войны в Испании — честный взгляд на идеализм, предательство и ужас войны.", "thoughts": []},
]

data.extend(new_books)

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

print('Done. Total books:', len(data))
for b in data[-8:]:
    print(b['id'], b['author'], '-', b['title'])
