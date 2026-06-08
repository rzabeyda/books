content = open('/root/books/webapp/app.js', encoding='utf-8').read()
old = "'блогеры':      'Блогеры'"
new = "'блогеры':      'Блогеры',\n  'цитаты':      'Цитаты'"
if 'цитаты' in content:
    print('уже есть')
elif old in content:
    open('/root/books/webapp/app.js', 'w', encoding='utf-8').write(content.replace(old, new, 1))
    print('OK')
else:
    print('not found')
