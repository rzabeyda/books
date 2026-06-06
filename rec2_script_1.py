import json

# Read existing books
with open('C:/books/books.json', encoding='utf-8') as f:
    books = json.load(f)

# New books to add (no thoughts yet)
new_books = [
  {"id":24,"title":"Думай и богатей","author":"Наполеон Хилл","cover":"dumay.jpg","world_reads":100000000,"world_reads_label":"100 млн+ копий","thoughts":[]},
  {"id":25,"title":"Целеустремлённая жизнь","author":"Рик Уоррен","cover":"cele_zhizn.jpg","world_reads":50000000,"world_reads_label":"50 млн+ копий","thoughts":[]},
  {"id":26,"title":"Ребёнок и уход за ним","author":"Бенджамин Спок","cover":"rebjonok.jpg","world_reads":50000000,"world_reads_label":"50 млн+ копий","thoughts":[]},
  {"id":27,"title":"Исцели свою жизнь","author":"Луиза Хей","cover":"isceli_zhizn.jpg","world_reads":50000000,"world_reads_label":"50 млн+ копий","thoughts":[]},
  {"id":28,"title":"7 навыков высокоэффективных людей","author":"Стивен Кови","cover":"7navykov.jpg","world_reads":40000000,"world_reads_label":"40 млн+ копий","thoughts":[]},
  {"id":29,"title":"Богатый папа, бедный папа","author":"Роберт Кийосаки","cover":"papa.jpg","world_reads":40000000,"world_reads_label":"40 млн+ копий","thoughts":[]},
  {"id":30,"title":"Дневник Анны Франк","author":"Анна Франк","cover":"dnevnik.jpg","world_reads":35000000,"world_reads_label":"35 млн+ копий","thoughts":[]},
  {"id":31,"title":"Секрет","author":"Ронда Берн","cover":"secret.jpg","world_reads":35000000,"world_reads_label":"35 млн+ копий","thoughts":[]},
  {"id":32,"title":"Как завоевать друзей и оказывать влияние на людей","author":"Дейл Карнеги","cover":"druzya.jpg","world_reads":30000000,"world_reads_label":"30 млн+ копий","thoughts":[]},
  {"id":33,"title":"Сила позитивного мышления","author":"Норман Пил","cover":"sila_poz_mysl.jpg","world_reads":20000000,"world_reads_label":"20 млн+ копий","thoughts":[]},
  {"id":34,"title":"Мужчины с Марса, женщины с Венеры","author":"Джон Грэй","cover":"venera.jpg","world_reads":15000000,"world_reads_label":"15 млн+ копий","thoughts":[]},
  {"id":35,"title":"Тонкое искусство пофигизма","author":"Марк Мэнсон","cover":"pofigism.jpg","world_reads":15000000,"world_reads_label":"15 млн+ копий","thoughts":[]},
  {"id":36,"title":"Вторники с Морри","author":"Митч Элбом","cover":"vtornik_s.jpg","world_reads":14000000,"world_reads_label":"14 млн+ копий","thoughts":[]},
  {"id":37,"title":"Долгий путь к свободе","author":"Нельсон Мандела","cover":"svoboda.jpg","world_reads":14000000,"world_reads_label":"14 млн+ копий","thoughts":[]},
  {"id":38,"title":"48 законов власти","author":"Роберт Грин","cover":"48.jpg","world_reads":5000000,"world_reads_label":"5 млн+ копий","thoughts":[]},
  {"id":39,"title":"Великая шахматная доска","author":"Збигнев Бжезинский","cover":"doska.jpg","world_reads":1000000,"world_reads_label":"1 млн+ копий","thoughts":[]},
  {"id":40,"title":"Библия","author":"Различные авторы","cover":"bibliya.jpg","world_reads":5000000000,"world_reads_label":"5 млрд+ копий","thoughts":[]},
  {"id":41,"title":"Коран","author":"Священный текст","cover":"koran.jpg","world_reads":800000000,"world_reads_label":"800 млн+ копий","thoughts":[]},
  {"id":42,"title":"Тора","author":"Священный текст","cover":"tora.jpg","world_reads":50000000,"world_reads_label":"50 млн+ копий","thoughts":[]},
  {"id":43,"title":"Неудобная правда для удобной жизни","author":"Антон Петряков","cover":"neudobnaya_pravda.jpg","world_reads":100000,"world_reads_label":"Бестселлер","thoughts":[]},
]

books.extend(new_books)

with open('C:/books/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

print(f'Итого книг: {len(books)}')
for b in books:
    print(f"{b['id']:2}. {b['title'][:40]} — {b['cover']}")
