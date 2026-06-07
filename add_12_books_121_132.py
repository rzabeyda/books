
import json

with open('/root/books/webapp/books.json', 'r') as f:
    books = json.load(f)

new_books = [
    {
        "id": 121,
        "title": "Зачем мы спим",
        "author": "Мэттью Уолкер",
        "cover": "covers/za4em_my_spim.jpg",
        "world_reads": 3000000,
        "world_reads_label": "Тираж 3млн+",
        "year": 2017,
        "genre": "саморазвитие",
        "description": "Учёный объясняет почему сон — важнейшая инвестиция в здоровье, мозг и долголетие, и что происходит когда мы его недооцениваем.",
        "thoughts": []
    },
    {
        "id": 122,
        "title": "Принципы",
        "author": "Рэй Далио",
        "cover": "covers/principy_rey.jpg",
        "world_reads": 3000000,
        "world_reads_label": "Тираж 3млн+",
        "year": 2017,
        "genre": "бизнес",
        "description": "Основатель крупнейшего хедж-фонда делится системой принципов для жизни и работы — как принимать лучшие решения и строить сильные команды.",
        "thoughts": []
    },
    {
        "id": 123,
        "title": "Эссенциализм",
        "author": "Грег МакКеон",
        "cover": "covers/essencialism.jpg",
        "world_reads": 2000000,
        "world_reads_label": "Тираж 2млн+",
        "year": 2014,
        "genre": "саморазвитие",
        "description": "Как делать меньше, но лучше — искусство сосредотачиваться только на том что действительно важно и отказываться от всего остального.",
        "thoughts": []
    },
    {
        "id": 124,
        "title": "Начни с вопроса «Почему»",
        "author": "Саймон Синек",
        "cover": "covers/na4ni_s_voprosy_po4emy.jpg",
        "world_reads": 2000000,
        "world_reads_label": "Тираж 2млн+",
        "year": 2009,
        "genre": "бизнес",
        "description": "Почему одни лидеры и компании вдохновляют людей, а другие нет — всё дело в том начинаешь ли ты с вопроса «зачем».",
        "thoughts": []
    },
    {
        "id": 125,
        "title": "Поток",
        "author": "Михай Чиксентмихайи",
        "cover": "covers/potok_mihaj.jpg",
        "world_reads": 1000000,
        "world_reads_label": "Тираж 1млн+",
        "year": 1990,
        "genre": "психология",
        "description": "Психолог исследует состояние полного погружения в деятельность — и объясняет как создавать условия для счастья и смысла.",
        "thoughts": []
    },
    {
        "id": 126,
        "title": "От нуля к единице",
        "author": "Питер Тиль",
        "cover": "covers/ot_nulja_k_edenice.jpg",
        "world_reads": 2000000,
        "world_reads_label": "Тираж 2млн+",
        "year": 2014,
        "genre": "бизнес",
        "description": "Сооснователь PayPal о том как строить компании создающие будущее — не копируя существующее, а создавая принципиально новое.",
        "thoughts": []
    },
    {
        "id": 127,
        "title": "Пять языков любви",
        "author": "Гэри Чепмен",
        "cover": "covers/5_jazykov_ljubvi.jpg",
        "world_reads": 20000000,
        "world_reads_label": "Тираж 20млн+",
        "year": 1992,
        "genre": "психология",
        "description": "Почему люди в отношениях чувствуют себя нелюбимыми — и как говорить на языке любви который понимает партнёр.",
        "thoughts": []
    },
    {
        "id": 128,
        "title": "Стив Джобс",
        "author": "Уолтер Айзексон",
        "cover": "covers/stiv_jobs_uolter.jpg",
        "world_reads": 8000000,
        "world_reads_label": "Тираж 8млн+",
        "year": 2011,
        "genre": "биографии",
        "description": "Полная биография основателя Apple — о гениальности, жестокости, перфекционизме и том как один человек изменил несколько индустрий.",
        "thoughts": []
    },
    {
        "id": 129,
        "title": "Эмоциональный интеллект",
        "author": "Дэниел Гоулман",
        "cover": "covers/emocionalny_intellekt.png",
        "world_reads": 5000000,
        "world_reads_label": "Тираж 5млн+",
        "year": 1995,
        "genre": "психология",
        "description": "Почему EQ важнее IQ — как умение понимать и управлять эмоциями определяет успех в жизни, работе и отношениях.",
        "thoughts": []
    },
    {
        "id": 130,
        "title": "Илон Маск",
        "author": "Уолтер Айзексон",
        "cover": "covers/ilon_musk_uolter.jpg",
        "world_reads": 4000000,
        "world_reads_label": "Тираж 4млн+",
        "year": 2023,
        "genre": "биографии",
        "description": "Биография самого противоречивого предпринимателя современности — о Tesla, SpaceX, Twitter и цене одержимости великими целями.",
        "thoughts": []
    },
    {
        "id": 131,
        "title": "Ненасильственное общение",
        "author": "Маршалл Розенберг",
        "cover": "covers/nenasilstvennoe_obwenie.jpg",
        "world_reads": 2000000,
        "world_reads_label": "Тираж 2млн+",
        "year": 1999,
        "genre": "психология",
        "description": "Как говорить и слушать так чтобы создавать связь а не конфликт — метод ненасильственного общения применимый везде.",
        "thoughts": []
    },
    {
        "id": 132,
        "title": "Тело",
        "author": "Билл Брайсон",
        "cover": "covers/telo_bill.jpg",
        "world_reads": 2000000,
        "world_reads_label": "Тираж 2млн+",
        "year": 2019,
        "genre": "саморазвитие",
        "description": "Увлекательное путешествие внутрь человеческого тела — как оно устроено, что умеет и почему является самым удивительным объектом во вселенной.",
        "thoughts": []
    },
]

existing_ids = {b['id'] for b in books}
added = 0
for nb in new_books:
    if nb['id'] not in existing_ids:
        books.append(nb)
        print(f"ID {nb['id']}: {nb['title']} — добавлен")
        added += 1

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

print(f'Добавлено: {added}. Итого книг: {len(books)}. Done.')
