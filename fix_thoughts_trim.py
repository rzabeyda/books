import json
with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

ids = [60,61,63,64,65,66,67,68,69,72,73,74,75,79,81,83]

for book in data:
    if book['id'] not in ids:
        continue
    for t in book['thoughts']:
        ex = t['example']
        if len(ex) <= 820:
            continue
        # Find last sentence boundary <= 810 chars
        target = ex[:815]
        # Try finding last period
        pos = target.rfind('.')
        if pos > 700:
            t['example'] = ex[:pos+1]
            continue
        # Try last em-dash phrase end (unlikely but fallback)
        pos = target.rfind('!')
        if pos > 700:
            t['example'] = ex[:pos+1]
            continue
        # Last resort: truncate at 810
        t['example'] = ex[:810]

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

# Verify
for book in data:
    if book['id'] in ids:
        lens = [len(t['example']) for t in book['thoughts']]
        bad = [(i, l) for i, l in enumerate(lens) if l < 700 or l > 820]
        status = 'OK' if not bad else f'BAD={bad}'
        print(f'ID={book["id"]} {book["title"][:22]}: min={min(lens)} max={max(lens)} {status}')
