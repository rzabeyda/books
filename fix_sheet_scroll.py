with open('/root/books/webapp/style.css', encoding='utf-8') as f:
    css = f.read()

add = '''
/* sheet-list scroll */
.sheet-list { overflow-y: auto; max-height: 60vh; }
'''

if 'sheet-list' not in css:
    css = css.rstrip() + '\n' + add
    with open('/root/books/webapp/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('OK: sheet-list overflow-y добавлен')
else:
    print('уже есть')
