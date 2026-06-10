content = open('/root/books/webapp/app.js').read()
old = "  'отношения':         'Отношения',"
new = "  'отношения':         'Отношения',\n  'стримеры':          'Стримеры',"
content = content.replace(old, new)
open('/root/books/webapp/app.js', 'w').write(content)
print('done')
