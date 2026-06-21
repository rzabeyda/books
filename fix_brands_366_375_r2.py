import json
with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

r2 = {
    (366,0): ' Возняк получил $800 за свою долю — сегодня это $200 млрд.',
    (367,9): ' Галочка без надписи — это высший уровень брендинга.',
    (371,3): ' Adidas создал модель «атлет как бренд».',
    (372,6): ' Страна-бренд сильнее любой рекламной кампании.',
}

for book in data:
    bid = book['id']
    for i, t in enumerate(book['thoughts']):
        if (bid, i) in r2:
            t['example'] = t['example'] + r2[(bid, i)]

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

ids = [366,367,371,372]
for book in data:
    if book['id'] in ids:
        dlens = len(book['description'])
        tlens = [len(t['example']) for t in book['thoughts']]
        t_bad = [(i,l) for i,l in enumerate(tlens) if l < 700 or l > 820]
        d_ok = 125 <= dlens <= 150
        status = 'OK' if d_ok and not t_bad else f'BAD desc={dlens} t={t_bad}'
        print(f'ID={book["id"]:3d} {book["title"][:18]:18s}: {status}')
