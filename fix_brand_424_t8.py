import json
with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

for book in data:
    if book['id'] == 424:
        t = book['thoughts'][8]
        ex = t['example']
        print(f'len={len(ex)}: {ex[-50:]}')
        pos = ex[:815].rfind('.')
        if pos > 700:
            t['example'] = ex[:pos+1]
            print(f'trimmed to {len(t["example"])}')

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

for book in data:
    if book['id'] == 424:
        dlens = len(book['description'])
        tlens = [len(t['example']) for t in book['thoughts']]
        t_bad = [(i,l) for i,l in enumerate(tlens) if l < 700 or l > 820]
        d_ok = 125 <= dlens <= 150
        status = 'OK' if d_ok and not t_bad else f'BAD desc={dlens} t={t_bad}'
        print(f'ID=424: {status}')
