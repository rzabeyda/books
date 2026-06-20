import json
with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

for book in data:
    if book['id'] == 582:
        book['thoughts'][8]['example'] += ' Место создаёт атмосферу которую нельзя выдумать.'
        break

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

for book in data:
    if book['id'] == 582:
        lens = [len(t['example']) for t in book['thoughts']]
        bad = [(i,l) for i,l in enumerate(lens) if l < 700 or l > 820]
        print(f'ID=582: min={min(lens)} max={max(lens)} {"OK" if not bad else bad}')
