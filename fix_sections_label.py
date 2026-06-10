content = open('/root/books/webapp/app.js').read()
old = "  'художественная':    'Художественная',"
new = "  'художественная':    'Художественная',\n  'отношения':         'Отношения',"
content = content.replace(old, new)
open('/root/books/webapp/app.js', 'w').write(content)
print('done')
