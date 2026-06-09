with open('/root/books/webapp/app.js', encoding='utf-8') as f:
    js = f.read()

old = "'<div class=\"detail-book-author\">' + b.author + '</div>' +"
new = "'<div class=\"detail-book-author\">' + b.author + '</div>' +\n    (b.genre ? '<div class=\"detail-genre\">' + (GENRE_LABELS[b.genre] || b.genre) + '</div>' : '') +"

if old in js:
    js = js.replace(old, new, 1)
    with open('/root/books/webapp/app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print('OK: жанр добавлен на детальную страницу')
else:
    print('NOT FOUND')
    idx = js.find('detail-book-author')
    print(repr(js[idx-10:idx+80]))
