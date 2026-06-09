
# ── 1. app.js: обновить GENRE_LABELS и добавить жанр на детальной странице ──
with open('/root/books/webapp/app.js', encoding='utf-8') as f:
    js = f.read()

# Обновить GENRE_LABELS
old_labels = """var GENRE_LABELS = {
  'саморазвитие': 'Саморазвитие',
  'психология':   'Психология',
  'бизнес':       'Бизнес',
  'nonfiction':   'Нон-фикшн',
  'классика':     'Классика',
  'мемуары':      'Мемуары',
  'биографии':    'Биографии',
  'история':      'История',
  'сказки':       'Сказки',
  'religion':     'Священные писания',
  'politics':     'Политика',
  'блогеры':      'Блогеры',
  'цитаты':      'Цитаты',
  'история успеха': 'История успеха',
};"""

new_labels = """var GENRE_LABELS = {
  'саморазвитие':      'Саморазвитие',
  'психология':        'Психология',
  'бизнес':            'Бизнес',
  'классика':          'Классика',
  'мемуары':           'Мемуары',
  'биографии':         'Биографии',
  'история':           'История',
  'сказки':            'Сказки',
  'блогеры':           'Блогеры',
  'цитаты':            'Цитаты',
  'история успеха':    'История успеха',
  'философия':         'Философия',
  'наука':             'Наука',
  'фэнтези':           'Фэнтези',
  'политика':          'Политика',
  'священные писания': 'Священные писания',
};"""

if old_labels in js:
    js = js.replace(old_labels, new_labels, 1)
    print('app.js: GENRE_LABELS обновлен')
else:
    print('app.js: GENRE_LABELS NOT FOUND')

# Найти место где рендерится детальная страница книги — добавить жанр
# Ищем строку с book-author в detail
old_detail = "'<div class=\"detail-author\">' + b.author + '</div>' +"
new_detail = "'<div class=\"detail-author\">' + b.author + '</div>' +" + """
      (b.genre ? '<div class=\"detail-genre\">' + (GENRE_LABELS[b.genre] || b.genre) + '</div>' : '') +"""

if old_detail in js:
    js = js.replace(old_detail, new_detail, 1)
    print('app.js: detail-genre добавлен')
else:
    print('app.js: detail-author NOT FOUND — ищем альтернативу')
    # показать контекст
    idx = js.find('detail-author')
    if idx != -1:
        print(repr(js[idx-20:idx+100]))

with open('/root/books/webapp/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

# ── 2. style.css: стиль для detail-genre ──
with open('/root/books/webapp/style.css', encoding='utf-8') as f:
    css = f.read()

if 'detail-genre' not in css:
    css = css.rstrip() + """

.detail-genre {
  font-size: 12px;
  color: var(--accent);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .07em;
  margin-top: 4px;
}
"""
    with open('/root/books/webapp/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('style.css: detail-genre добавлен')
else:
    print('style.css: detail-genre уже есть')

print('DONE')
