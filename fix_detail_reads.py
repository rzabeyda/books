
# app.js
with open('/root/books/webapp/app.js', 'r') as f:
    js = f.read()

old = "'<div class=\"detail-badge\">' + b.thoughts.length + ' главных мыслей</div>' +"
new = ("'<div class=\"detail-badge\">' + b.thoughts.length + ' главных мыслей</div>' +\n"
       "    (b.world_reads_label ? '<div class=\"detail-reads\">' + b.world_reads_label + '</div>' : '') +")

if old in js:
    js = js.replace(old, new, 1)
    print('OK: тираж добавлен в детальную страницу')
else:
    print('ERROR: pattern not found')

with open('/root/books/webapp/app.js', 'w') as f:
    f.write(js)

# style.css
with open('/root/books/webapp/style.css', 'r') as f:
    css = f.read()

css += '\n.detail-reads { font-size: 12px; color: #888; margin-top: 4px; }\n'

with open('/root/books/webapp/style.css', 'w') as f:
    f.write(css)

print('Done.')
