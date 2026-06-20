import json
with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

r2 = {
    (263,7): ' Это не детская книга.',
    (265,7): ' Красота без совести — оружие.',
    (267,1): ' Пастернак это знал.',
    (267,6): ' Оба виноваты и оба жертвы.',
    (268,3): ' Достоевский описал это точно.',
    (268,6): ' Но механизм он описал верно.',
    (268,7): ' Иногда это — начало выхода.',
    (304,1): ' Маркес показывает: ожидание бывает активным.',
    (304,7): ' Диккенс называл его «воплощением соблазна».',
    (305,2): ' Зимбардо назвал это «эффектом Люцифера».',
    (308,5): ' Это важнейшее разграничение.',
}

for book in data:
    bid = book['id']
    for i, t in enumerate(book['thoughts']):
        if (bid, i) in r2:
            t['example'] = t['example'] + r2[(bid, i)]

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

ids = [263,265,267,268,304,305,308]
for book in data:
    if book['id'] in ids:
        lens = [len(t['example']) for t in book['thoughts']]
        bad = [(i,l) for i,l in enumerate(lens) if l < 700 or l > 820]
        status = 'OK' if not bad else f'BAD={bad}'
        print(f'ID={book["id"]:3d}: min={min(lens)} max={max(lens)} {status}')
