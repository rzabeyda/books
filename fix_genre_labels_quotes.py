import re

with open('/root/books/webapp/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

old = "'блогеры': 'Блогеры'"
new = "'блогеры': 'Блогеры', 'цитаты': 'Цитаты'"

if "'цитаты'" in content:
    print("Уже есть 'цитаты' в GENRE_LABELS")
elif old in content:
    content = content.replace(old, new, 1)
    with open('/root/books/webapp/app.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK: добавлено 'цитаты': 'Цитаты' в GENRE_LABELS")
else:
    print("ОШИБКА: не нашёл 'блогеры' в app.js — проверь файл")
