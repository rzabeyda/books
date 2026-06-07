import json

# --- books.json ---
with open('/root/books/webapp/books.json', 'r') as f:
    books = json.load(f)

# Распределение по жанрам
психология = {4,5,9,13,14,15,16,20,21,22,23,26,34,45,46,47,48,49}
саморазвитие = {2,6,8,17,18,19,25,27,28,31,32,33,35,43,51,92,93,94,95,96,112}
бизнес = {24,29,38,50,59,86}
# остаток nonfiction: 3,7,10,11,12,56,87,91,102,104

for b in books:
    if b['id'] in психология:
        b['genre'] = 'психология'
    elif b['id'] in саморазвитие:
        b['genre'] = 'саморазвитие'
    elif b['id'] in бизнес:
        b['genre'] = 'бизнес'

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

from collections import Counter
c = Counter(b['genre'] for b in books)
for g, n in sorted(c.items(), key=lambda x: -x[1]):
    print(f'{g}: {n}')

print('Done.')

# --- app.js ---
with open('/root/books/webapp/app.js', 'r') as f:
    js = f.read()

old_opt = """var GENRE_OPTIONS = [
  { key: 'all',       label: 'Все книги' },
  { key: 'nonfiction',label: 'Нон-фикшн' },
  { key: 'классика',  label: 'Классика' },
  { key: 'сказки',    label: 'Сказки' },
  { key: 'мемуары',   label: 'Мемуары' },
  { key: 'история',   label: 'История' },
  { key: 'religion',  label: 'Священные писания' },
  { key: 'politics',  label: 'Политика' },
];"""

new_opt = """var GENRE_OPTIONS = [
  { key: 'all',          label: 'Все книги' },
  { key: 'саморазвитие', label: 'Саморазвитие' },
  { key: 'психология',   label: 'Психология' },
  { key: 'бизнес',       label: 'Бизнес' },
  { key: 'nonfiction',   label: 'Нон-фикшн' },
  { key: 'классика',     label: 'Классика' },
  { key: 'мемуары',      label: 'Мемуары' },
  { key: 'история',      label: 'История' },
  { key: 'сказки',       label: 'Сказки' },
  { key: 'religion',     label: 'Священные писания' },
  { key: 'politics',     label: 'Политика' },
];"""

old_gen = """var GENRES = [
  { key: 'nonfiction', label: 'Нон-фикшн' },
  { key: 'классика',   label: 'Классика' },
  { key: 'сказки',     label: 'Сказки' },
  { key: 'мемуары',    label: 'Мемуары' },
  { key: 'история',    label: 'История' },
  { key: 'religion',   label: 'Священные писания' },
  { key: 'politics',   label: 'Политика' },
];"""

new_gen = """var GENRES = [
  { key: 'саморазвитие', label: 'Саморазвитие' },
  { key: 'психология',   label: 'Психология' },
  { key: 'бизнес',       label: 'Бизнес' },
  { key: 'nonfiction',   label: 'Нон-фикшн' },
  { key: 'классика',     label: 'Классика' },
  { key: 'мемуары',      label: 'Мемуары' },
  { key: 'история',      label: 'История' },
  { key: 'сказки',       label: 'Сказки' },
  { key: 'religion',     label: 'Священные писания' },
  { key: 'politics',     label: 'Политика' },
];"""

if old_opt in js:
    js = js.replace(old_opt, new_opt)
    print('OK: GENRE_OPTIONS updated')
else:
    print('ERROR: GENRE_OPTIONS not found')

if old_gen in js:
    js = js.replace(old_gen, new_gen)
    print('OK: GENRES updated')
else:
    print('ERROR: GENRES not found')

with open('/root/books/webapp/app.js', 'w') as f:
    f.write(js)
