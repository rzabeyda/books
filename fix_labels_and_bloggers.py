import json, re

# --- books.json: fix world_reads_label ---
with open('/root/books/webapp/books.json', 'r') as f:
    books = json.load(f)

for b in books:
    if b.get('world_reads_label'):
        # "25 млн+ копий" → "Тираж 25млн+"
        m = re.search(r'([\d,.]+\s*млн)', b['world_reads_label'])
        if m:
            num = m.group(1).replace(' ', '')
            b['world_reads_label'] = f'Тираж {num}+'

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

import json
books2 = json.load(open('/root/books/webapp/books.json'))
for b in books2[:3]:
    if b.get('world_reads_label'):
        print(b['title'], '→', b['world_reads_label'])

# --- app.js: add блогеры genre ---
with open('/root/books/webapp/app.js', 'r') as f:
    js = f.read()

old_opt = "  { key: 'politics',     label: 'Политика' },\n];"
new_opt = "  { key: 'politics',     label: 'Политика' },\n  { key: 'блогеры',      label: 'Блогеры' },\n];"

old_gen = "  { key: 'politics',   label: 'Политика' },\n];"
new_gen = "  { key: 'politics',   label: 'Политика' },\n  { key: 'блогеры',    label: 'Блогеры' },\n];"

if old_opt in js:
    js = js.replace(old_opt, new_opt)
    print('OK: GENRE_OPTIONS — блогеры добавлен')
else:
    print('ERROR: GENRE_OPTIONS end not found')

if old_gen in js:
    js = js.replace(old_gen, new_gen)
    print('OK: GENRES — блогеры добавлен')
else:
    print('ERROR: GENRES end not found')

with open('/root/books/webapp/app.js', 'w') as f:
    f.write(js)

print('Done.')
