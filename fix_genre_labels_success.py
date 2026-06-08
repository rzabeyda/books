content = open('/root/books/webapp/app.js', encoding='utf-8').read()
old = "'цитаты':      'Цитаты'"
new = "'цитаты':      'Цитаты',\n  'история успеха': 'История успеха'"
if 'история успеха' in content:
    print('уже есть')
elif old in content:
    open('/root/books/webapp/app.js', 'w', encoding='utf-8').write(content.replace(old, new, 1))
    print('OK')
else:
    print('not found')
