import json

def trim_to_fit(title, example, max_total=800):
    total = len(title) + len(example)
    if total <= max_total:
        return example
    max_ex = max_total - len(title)
    chunk = example[:max_ex]
    for sep in ['. ', '! ', '? ']:
        pos = chunk.rfind(sep)
        if pos > max_ex - 200:
            return chunk[:pos+1]
    pos = chunk.rfind(' ')
    return chunk[:pos] + '.'

with open('/root/books/webapp/books.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

for b in books:
    bid = b['id']
    if bid == 20:
        b['description'] = "10 идей о том почему дети всё больше ориентированы на сверстников — и как родителю вернуть себе роль главной привязанности."
        for t in b['thoughts']:
            t['example'] = trim_to_fit(t['title'], t['example'])
    elif bid == 26:
        b['description'] = "Доктор Спок о первых годах жизни: доверяй себе, люби без страха избаловать и помни что каждый ребёнок уникален."
        for i, t in enumerate(b['thoughts']):
            if i == 0:
                t['example'] = trim_to_fit(t['title'], t['example'])
            elif i == 5:
                t['example'] += " Объяснение важнее запрета."

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

print("=== VERIFY 20, 26 ===")
issues = []
for b in books:
    if b['id'] not in [20, 26]: continue
    d = len(b['description'])
    ds = 'OK' if 125<=d<=150 else 'BAD'
    if ds != 'OK': issues.append(f"ID {b['id']} DESC {d}: {b['description']}")
    for i, t in enumerate(b['thoughts']):
        total = len(t['title']) + len(t['example'])
        s = 'OK' if 700<=total<=800 else ('SHORT' if total<700 else 'LONG')
        if s != 'OK': issues.append(f"ID {b['id']} t{i} {s}={total}: {t['title'][:40]}")
if issues:
    print("ISSUES:"); [print(" ", x) for x in issues]
else:
    print("All OK!")
