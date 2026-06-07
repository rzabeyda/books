
# Добавляем description под автором в app.js и стиль в style.css

with open('/root/books/webapp/app.js', 'r') as f:
    js = f.read()

old = "    '<div class=\"detail-book-author\">' + b.author + '</div>' +\n    (b.world_reads_label"
new = "    '<div class=\"detail-book-author\">' + b.author + '</div>' +\n    (b.description ? '<div class=\"detail-description\">' + b.description + '</div>' : '') +\n    (b.world_reads_label"

if old in js:
    js = js.replace(old, new, 1)
    print('OK: description добавлен в app.js')
else:
    print('ERROR: pattern not found in app.js')

with open('/root/books/webapp/app.js', 'w') as f:
    f.write(js)

with open('/root/books/webapp/style.css', 'r') as f:
    css = f.read()

desc_style = '\n.detail-description { font-size: 12px; color: #888; margin-top: 6px; line-height: 1.5; }\n'
if '.detail-description' not in css:
    css += desc_style
    print('OK: стиль detail-description добавлен')
else:
    print('стиль уже есть')

with open('/root/books/webapp/style.css', 'w') as f:
    f.write(css)

print('Done.')
