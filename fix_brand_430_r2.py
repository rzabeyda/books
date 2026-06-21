import json
with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

for book in data:
    if book['id'] == 430:
        book['thoughts'][3]['example'] += ' Стив Балмер запомнился своими эмоциональными выступлениями. Сейчас владеет LA Clippers.'

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

for book in data:
    if book['id'] == 430:
        dlens = len(book['description'])
        tlens = [len(t['example']) for t in book['thoughts']]
        t_bad = [(i,l) for i,l in enumerate(tlens) if l < 700 or l > 820]
        d_ok = 125 <= dlens <= 150
        print(f'ID=430: desc={dlens} {"OK" if d_ok and not t_bad else f"BAD t={t_bad}"}')
