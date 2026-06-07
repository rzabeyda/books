
with open('/root/books/webapp/app.js', 'r') as f:
    js = f.read()

old = (
    "    '<div class=\"detail-book-author\">' + b.author + '</div>' +\n"
    "    '<div class=\"detail-badge\">' + b.thoughts.length + ' главных мыслей</div>' +\n"
    "    (b.world_reads_label ? '<div class=\"detail-reads\">' + b.world_reads_label + '</div>' : '') +\n"
    "    (b.year ? '<div class=\"detail-book-year\">' + (b.year < 0 ? Math.abs(b.year) + ' г. до н.э.' : b.year + ' г.') + '</div>' : '') +\n"
    "    '</div></div>' +\n"
    "    '<div class=\"thoughts-list\">' + thoughtsHtml + '</div>' +"
)

new = (
    "    '<div class=\"detail-book-author\">' + b.author + '</div>' +\n"
    "    (b.world_reads_label ? '<div class=\"detail-reads\">' + b.world_reads_label + '</div>' : '') +\n"
    "    (b.year ? '<div class=\"detail-book-year\">' + (b.year < 0 ? Math.abs(b.year) + ' г. до н.э.' : b.year + ' г.') + '</div>' : '') +\n"
    "    '</div></div>' +\n"
    "    '<div class=\"thoughts-title\">' + b.thoughts.length + ' главных мыслей</div>' +\n"
    "    '<div class=\"thoughts-list\">' + thoughtsHtml + '</div>' +"
)

if old in js:
    js = js.replace(old, new, 1)
    print('OK: бейдж перемещён под картинку')
else:
    print('ERROR: pattern not found')

with open('/root/books/webapp/app.js', 'w') as f:
    f.write(js)

# CSS
with open('/root/books/webapp/style.css', 'r') as f:
    css = f.read()

# тираж — жёлтый
css = css.replace(
    '.detail-reads { font-size: 12px; color: #888; margin-top: 4px; }',
    '.detail-reads { font-size: 12px; color: var(--accent); font-weight: 600; margin-top: 4px; }'
)

# год — голубой
css = css.replace(
    '.detail-book-year { font-size: 12px; color: #666; margin-top: 2px; }',
    '.detail-book-year { font-size: 12px; color: #6ab3f5; margin-top: 2px; }'
)

# thoughts-title — стиль как был у detail-badge (жёлтый uppercase)
css = css.replace(
    '.thoughts-title { font-size: 13px; font-weight: 600; margin-bottom: 10px; }',
    '.thoughts-title { font-size: 11px; font-weight: 700; color: var(--accent); letter-spacing: .08em; text-transform: uppercase; margin: 14px 0 10px; }'
)

with open('/root/books/webapp/style.css', 'w') as f:
    f.write(css)

print('OK: цвета обновлены')
print('Done.')
