
# Добавляем жанр "биографии" в app.js и проставляем его нужным книгам

with open('/root/books/webapp/app.js', 'r') as f:
    js = f.read()

# GENRE_OPTIONS — добавляем после мемуары
old_opt = "  { key: 'мемуары',      label: 'Мемуары' },"
new_opt = "  { key: 'мемуары',      label: 'Мемуары' },\n  { key: 'биографии',    label: 'Биографии' },"

if old_opt in js:
    js = js.replace(old_opt, new_opt, 1)
    print('OK: биографии добавлены в GENRE_OPTIONS')
else:
    print('ERROR: GENRE_OPTIONS мемуары not found')

# GENRES — добавляем после мемуары
old_genres = "  { key: 'мемуары',      label: 'Мемуары' },\n  { key: 'история',"
new_genres = "  { key: 'мемуары',      label: 'Мемуары' },\n  { key: 'биографии',    label: 'Биографии' },\n  { key: 'история',"

if old_genres in js:
    js = js.replace(old_genres, new_genres, 1)
    print('OK: биографии добавлены в GENRES')
else:
    print('ERROR: GENRES мемуары not found')

with open('/root/books/webapp/app.js', 'w') as f:
    f.write(js)

# Проставляем жанр биографии нужным книгам в books.json
import json

with open('/root/books/webapp/books.json', 'r') as f:
    books = json.load(f)

# Книги которые должны быть в биографиях
bio_ids = {
    128: 'Стив Джобс',
    130: 'Илон Маск',
    37:  'Долгая дорога к свободе',   # Мандела
}

updated = 0
for b in books:
    if b['id'] in bio_ids:
        old_genre = b.get('genre', '')
        b['genre'] = 'биографии'
        print(f"ID {b['id']}: {b['title']} — жанр {old_genre} → биографии")
        updated += 1

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

print(f'Обновлено книг: {updated}. Done.')
