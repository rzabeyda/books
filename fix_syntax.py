with open('/root/books/webapp/app.js', encoding='utf-8') as f:
    js = f.read()

bad = "  GENRE_OPTIONS = [{ key: 'all', label: 'Все книги' }].concat(GENRES);\n}).join('');\n}"
good = "  GENRE_OPTIONS = [{ key: 'all', label: 'Все книги' }].concat(GENRES);\n}"

if bad in js:
    js = js.replace(bad, good, 1)
    with open('/root/books/webapp/app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print('OK: синтаксическая ошибка исправлена')
else:
    print('NOT FOUND:', repr(bad[:60]))
    # показать контекст
    idx = js.find("]).join('')")
    if idx != -1:
        print('найдено join в:', repr(js[idx-100:idx+50]))
