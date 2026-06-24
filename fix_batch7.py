import json

def trim(title, example, max_total=800):
    max_ex = max_total - len(title)
    if len(example) <= max_ex:
        return example
    cut = example[:max_ex]
    for sep in ['. ', '! ', '? ']:
        idx = cut.rfind(sep)
        if idx > max_ex - 120:
            return cut[:idx+1]
    return cut.rstrip()

with open('/root/books/webapp/books.json', encoding='utf-8') as f:
    books = json.load(f)

fix_map = {
    905: [0, 2, 3, 6, 7, 8, 9],
    906: [0, 1, 2, 3, 4, 6, 8],
    907: [0, 5, 9],
    908: [0, 1, 3, 5, 6, 7, 8],
    909: [1, 2, 3, 4, 5, 6],
    910: [2, 4, 5, 7, 8, 9],
    911: [1, 2, 3, 4, 5, 7, 9],
}

for b in books:
    bid = b['id']
    if bid not in fix_map:
        continue
    for i in fix_map[bid]:
        t = b['thoughts'][i]
        t['example'] = trim(t['title'], t['example'])

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

errors = []
for b in books:
    if b['id'] not in fix_map:
        continue
    for i, t in enumerate(b['thoughts']):
        total = len(t['title']) + len(t['example'])
        if not (600 <= total <= 800):
            errors.append(f"  {b['id']} t{i}: {total}")

if errors:
    print("ОШИБКИ:"); [print(e) for e in errors]
else:
    print("Все OK!")
