import json
with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

r4 = {
    (515,6): ' Именно этот вопрос и есть суть книги.',
    (516,2): ' Две перспективы дополняют а не отменяют друг друга.',
    (516,6): ' Молчание — тоже выбор.',
    (519,4): ' Ремарк не теоретизировал — он помнил.',
}

for book in data:
    bid = book['id']
    for i, t in enumerate(book['thoughts']):
        if (bid, i) in r4:
            t['example'] = t['example'] + r4[(bid, i)]

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

ids = [515,516,519]
for book in data:
    if book['id'] in ids:
        lens = [len(t['example']) for t in book['thoughts']]
        bad = [(i,l) for i,l in enumerate(lens) if l < 700 or l > 820]
        status = 'OK' if not bad else f'BAD={bad}'
        print(f'ID={book["id"]:3d}: min={min(lens)} max={max(lens)} {status}')
