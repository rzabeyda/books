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
    890: [1, 3, 4, 5, 6, 7, 8, 9],
    891: [1, 2, 3, 4, 7, 8],
    892: [0, 1, 3, 4, 5, 7, 8, 9],
    893: [0, 1, 2, 3, 5, 6, 7, 8, 9],
    894: [1, 3, 5, 6, 7, 9],
}

for b in books:
    bid = b['id']
    if bid == 890:
        b['description'] = "Джим Аль-Халили открывает квантовую биологию — как квантовые эффекты лежат в основе фотосинтеза, обоняния и навигации птиц в живой клетке."
    if bid not in fix_map:
        continue
    for i in fix_map[bid]:
        t = b['thoughts'][i]
        t['example'] = trim(t['title'], t['example'])

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

errors = []
for b in books:
    if b['id'] not in fix_map and b['id'] != 890:
        continue
    dlen = len(b['description'])
    if not (125 <= dlen <= 150):
        errors.append(f"DESC {b['id']}: {dlen}")
    for i, t in enumerate(b['thoughts']):
        total = len(t['title']) + len(t['example'])
        if not (600 <= total <= 800):
            errors.append(f"  {b['id']} t{i}: {total}")

if errors:
    print("ОШИБКИ:"); [print(e) for e in errors]
else:
    print("Все OK!")
