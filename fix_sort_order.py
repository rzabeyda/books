content = open('/root/books/webapp/app.js').read()
old = "  { key: 'new',         label: 'Новое' },\n  { key: 'sales',       label: 'Тираж' },"
new = "  { key: 'sales',       label: 'Тираж' },\n  { key: 'new',         label: 'Новое' },"
content = content.replace(old, new)
open('/root/books/webapp/app.js', 'w').write(content)
print('done')
