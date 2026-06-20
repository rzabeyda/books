import json
with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

r3 = {
    (319,5): ' Так.',
    (319,8): ' Именно поэтому Кафка точнее историков: он описал механизм а не событие. Это работает в любую эпоху.',
}

for book in data:
    bid = book['id']
    for i, t in enumerate(book['thoughts']):
        if (bid, i) in r3:
            t['example'] = t['example'] + r3[(bid, i)]

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

for book in data:
    if book['id'] == 319:
        lens = [len(t['example']) for t in book['thoughts']]
        bad = [(i,l) for i,l in enumerate(lens) if l < 700 or l > 820]
        status = 'OK' if not bad else f'BAD={bad}'
        print(f'ID=319: min={min(lens)} max={max(lens)} {status}')
