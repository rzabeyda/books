import json, re

def trim(title, example, max_total=800):
    max_ex = max_total - len(title)
    if len(example) <= max_ex:
        return example
    cut = example[:max_ex]
    for sep in ['. ', '! ', '? ']:
        idx = cut.rfind(sep)
        if idx > max_ex - 100:
            return cut[:idx+1]
    return cut.rstrip()

with open('/root/books/webapp/books.json', encoding='utf-8') as f:
    books = json.load(f)

fix_ids = {878, 879, 880, 881, 882, 883}
fix_thoughts = {
    878: [7, 8, 9],
    879: [1, 3, 8],
    880: [4, 6],
    881: [0, 2, 3, 4, 5, 6],
    882: [1, 4, 5, 8, 9],
    883: [5, 7, 8],
}

for b in books:
    if b['id'] not in fix_ids:
        continue
    idxs = fix_thoughts.get(b['id'], [])
    for i in idxs:
        t = b['thoughts'][i]
        t['example'] = trim(t['title'], t['example'])

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

errors = []
for b in books:
    if b['id'] not in fix_ids:
        continue
    for i, t in enumerate(b['thoughts']):
        total = len(t['title']) + len(t['example'])
        if not (600 <= total <= 800):
            errors.append(f"  {b['id']} t{i}: {total}")

if errors:
    print("ОШИБКИ:"); [print(e) for e in errors]
else:
    print("Все OK!")
