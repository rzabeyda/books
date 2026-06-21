import json
with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

for book in data:
    if book['id'] == 377:
        book['description'] = 'Фердинанд создал Volkswagen для Гитлера. Его сын создал автомобиль мечты. История о семье, гонках и самом прибыльном автопроизводителе мира.'
    if book['id'] == 380:
        t = book['thoughts'][8]
        t['example'] = t['example'] + ' Audi строит будущее.'

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

for book in data:
    if book['id'] in [377, 380]:
        dlens = len(book['description'])
        tlens = [len(t['example']) for t in book['thoughts']]
        t_bad = [(i,l) for i,l in enumerate(tlens) if l < 700 or l > 820]
        d_ok = 125 <= dlens <= 150
        print(f'ID={book["id"]:3d}: desc={dlens} {"OK" if d_ok and not t_bad else f"BAD t={t_bad}"}')
