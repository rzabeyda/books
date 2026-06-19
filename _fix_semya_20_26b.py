import json

with open('/root/books/webapp/books.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

# Print current state
for b in books:
    if b['id'] not in [20, 26]: continue
    print(f"ID {b['id']}: desc={len(b['description'])}")
    for i, t in enumerate(b['thoughts']):
        total = len(t['title']) + len(t['example'])
        if total < 700:
            print(f"  t{i} SHORT={total} title={len(t['title'])}: {t['title']}")
            print(f"    example ends: ...{t['example'][-80:]}")

# Fix book 20 descriptions and short thoughts
fixes = {}
for b in books:
    bid = b['id']
    if bid == 20:
        b['description'] = "10 главных идей о том почему дети ориентированы на сверстников и как вернуть себе роль ключевой привязанности в жизни ребёнка."
        for i, t in enumerate(b['thoughts']):
            total = len(t['title']) + len(t['example'])
            if total < 700:
                need = 700 - total
                if i == 0:
                    t['example'] += " Именно этой потере привязанности посвящена книга — и именно восстановление связи с родителем Нойфельд считает ключом к здоровому развитию ребёнка."
                elif i == 7:
                    t['example'] += " Нойфельд настаивает: ребёнку нужно разрешение просто быть — без продукта, без цели, без результата. Только тогда созревает то что нельзя натренировать."
    elif bid == 26:
        b['description'] = "Доктор Спок о первых годах жизни: доверяй себе, люби без страха избаловать, и помни — каждый ребёнок уникален и сам знает что ему нужно."

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

print("=== VERIFY ===")
for b in books:
    if b['id'] not in [20, 26]: continue
    d = len(b['description'])
    ds = 'OK' if 125<=d<=150 else f'BAD({d})'
    print(f"ID {b['id']} desc={d} {ds}")
    for i, t in enumerate(b['thoughts']):
        total = len(t['title']) + len(t['example'])
        s = 'OK' if 700<=total<=800 else ('SHORT' if total<700 else f'LONG')
        if s != 'OK': print(f"  t{i} {s}={total}")
print("Done.")
