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

appends = {
    213: {
        4: " Это навык который нарабатывается только через практику на платформе.",
        5: " Первые связи в сообществе — фундамент карьеры на годы вперёд.",
        6: " Готовность к трансформации отличает авторов с долгой карьерой.",
        7: " Возврат с энергией сильнее непрерывного присутствия на износе.",
        8: " Сильный бренд открывает форматы которые одиночке недоступны.",
        9: " Долгожитель платформы — это живая карта её изменений за годы.",
    },
    214: {
        2: " Техническая экспертиза удерживает аудиторию энтузиастов надолго.",
        6: " Редкий доступ — итог многолетней репутации а не случая.",
    },
    218: {
        4: " Семья делает блогера человеком а не просто экранным персонажем.",
        7: " Дети которые выросли с блогером — самая преданная аудитория.",
    },
    220: {
        2: " Честность без возраста создаёт доверие которое удерживает аудиторию.",
    },
}

with open('/root/books/webapp/books.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

target = set(appends.keys())
for b in books:
    bid = b['id']
    if bid not in target: continue
    for i, t in enumerate(b['thoughts']):
        if bid in appends and i in appends[bid]:
            t['example'] += appends[bid][i]
        t['example'] = trim_to_fit(t['title'], t['example'])

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

print("=== VERIFY 4d ===")
issues = []
ids_check = {213, 214, 218, 220, 226}
for b in books:
    if b['id'] not in ids_check: continue
    for i, t in enumerate(b['thoughts']):
        total = len(t['title']) + len(t['example'])
        s = 'OK' if 700 <= total <= 800 else ('SHORT' if total < 700 else 'LONG')
        if s != 'OK': issues.append(f"ID {b['id']} t{i} {s}={total}")
if issues:
    print("ISSUES:"); [print(" ", x) for x in issues]
else:
    print("All OK!")
