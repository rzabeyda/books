
with open('/root/books/webapp/app.js', 'r') as f:
    js = f.read()

old = (
    "    '<div class=\"detail-book-title\">' + b.title + '</div>' +\n"
    "    '<div class=\"detail-book-author\">' + b.author + '</div>' +\n"
    "    (b.description ? '<div class=\"detail-description\">' + b.description + '</div>' : '') +\n"
    "    (b.world_reads_label ? '<div class=\"detail-reads\">' + b.world_reads_label + '</div>' : '') +\n"
    "    (b.year ? '<div class=\"detail-book-year\">' + (b.year < 0 ? Math.abs(b.year) + ' г. до н.э.' : b.year + ' г.') + '</div>' : '') +"
)

new = (
    "    '<div class=\"detail-book-title\">' + b.title +"
    " (b.year ? '<span class=\"detail-title-year\">' + (b.year < 0 ? Math.abs(b.year) + ' г. до н.э.' : b.year + ' г.') + '</span>' : '') +"
    " '</div>' +\n"
    "    '<div class=\"detail-book-author\">' + b.author + '</div>' +\n"
    "    (b.description ? '<div class=\"detail-description\">' + b.description + '</div>' : '') +"
)

if old in js:
    js = js.replace(old, new, 1)
    print('OK: год перенесён в заголовок, тираж убран')
else:
    print('ERROR: pattern not found')

with open('/root/books/webapp/app.js', 'w') as f:
    f.write(js)

# CSS: стиль года в заголовке
with open('/root/books/webapp/style.css', 'r') as f:
    css = f.read()

year_style = '\n.detail-title-year { font-size: 13px; color: #6ab3f5; font-weight: 400; margin-left: 6px; }\n'
if '.detail-title-year' not in css:
    css += year_style
    print('OK: стиль detail-title-year добавлен')

with open('/root/books/webapp/style.css', 'w') as f:
    f.write(css)

print('Done.')
