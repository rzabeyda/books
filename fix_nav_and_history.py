import json

# --- app.js ---
with open('/root/books/webapp/app.js', 'r') as f:
    js = f.read()

# Add история to GENRE_OPTIONS
old_opt = "  { key: 'мемуары',   label: 'Мемуары' },\n  { key: 'religion',  label: 'Священные писания' },"
new_opt = "  { key: 'мемуары',   label: 'Мемуары' },\n  { key: 'история',   label: 'История' },\n  { key: 'religion',  label: 'Священные писания' },"
if old_opt in js:
    js = js.replace(old_opt, new_opt)
    print('OK: GENRE_OPTIONS updated')
else:
    print('ERROR: GENRE_OPTIONS pattern not found')

# Add история to GENRES
old_gen = "  { key: 'мемуары',    label: 'Мемуары' },\n  { key: 'religion',   label: 'Священные писания' },"
new_gen = "  { key: 'мемуары',    label: 'Мемуары' },\n  { key: 'история',    label: 'История' },\n  { key: 'religion',   label: 'Священные писания' },"
if old_gen in js:
    js = js.replace(old_gen, new_gen)
    print('OK: GENRES updated')
else:
    print('ERROR: GENRES pattern not found')

# Remove book title from nav
old_nav = "  document.getElementById('detail-title-top').textContent = b.title;\n"
if old_nav in js:
    js = js.replace(old_nav, '')
    print('OK: nav title removed from JS')
else:
    print('ERROR: nav title JS line not found')

with open('/root/books/webapp/app.js', 'w') as f:
    f.write(js)

# --- index.html ---
with open('/root/books/webapp/index.html', 'r') as f:
    html = f.read()

old_span = '        <span id="detail-title-top" class="detail-title-top"></span>\n'
if old_span in html:
    html = html.replace(old_span, '')
    print('OK: nav title span removed from HTML')
else:
    print('ERROR: nav title span not found in HTML')

with open('/root/books/webapp/index.html', 'w') as f:
    f.write(html)

# --- books.json: move sapiens(1) and kratkiy_kurs(71) to история ---
with open('/root/books/webapp/books.json', 'r') as f:
    books = json.load(f)

history_ids = {1, 71}
for b in books:
    if b['id'] in history_ids:
        old = b['genre']
        b['genre'] = 'история'
        print(f"ID {b['id']}: {b['title']} | {old} → история")

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

print('Done.')
