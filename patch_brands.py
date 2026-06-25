import json

with open('/root/books/webapp/books.json', encoding='utf-8') as f:
    books = json.load(f)

# Fix descriptions
desc_fixes = {
    941: "Французский ювелирный дом создававший украшения для королей и магараджей — ювелир королей и король всех ювелиров с 1847.",
    942: "Французский дом высокой моды возродивший женственность после войны — New Look Кристиана Диора изменил мировую моду навек.",
}

# Fix thought examples
thought_fixes = {
    940: {
        3: " Дом который казался ушедшим в прошлое навсегда вернулся сильнее чем когда-либо.",
        4: " Он не просто провоцировал — он точно знал зачем это делает и каждый раз оказывался прав.",
        8: " История Balenciaga — урок о том что великое наследие нуждается в правильном менеджменте.",
    },
    942: {
        3: " Каждый из них доказывал что великая марка способна пережить смену творческого лидера.",
        4: " Личная история создателя всегда живёт в продукте — люди это чувствуют даже не зная деталей.",
    },
    945: {
        8: " Это фундаментальный принцип дизайна: создавай то что не привязано ко времени — и время тебя не победит.",
    },
}

for b in books:
    if b['id'] in desc_fixes:
        b['description'] = desc_fixes[b['id']]
    if b['id'] in thought_fixes:
        for idx, addition in thought_fixes[b['id']].items():
            b['thoughts'][idx]['example'] += addition

# verify
print("Описания:")
for b in books:
    if b['id'] in desc_fixes:
        l = len(b['description'])
        mark = 'OK' if 125 <= l <= 150 else f'!!! ({l})'
        print(f"  {b['title']}: {l} {mark}")

print("\nМысли:")
ids_to_check = {940, 942, 945}
all_ok = True
for b in books:
    if b['id'] in ids_to_check:
        bad = []
        for i, t in enumerate(b['thoughts']):
            l = len(t['title']) + len(t['example'])
            if not (600 <= l <= 800):
                bad.append(f"{i+1}:{l}")
        if bad:
            print(f"  {b['title']} ПРОБЛЕМЫ: {bad}")
            all_ok = False
        else:
            print(f"  {b['title']}: все OK")

# Check new books descriptions too
print("\nВсе новые книги 940-946:")
for b in books:
    if 940 <= b['id'] <= 946:
        dl = len(b['description'])
        dmark = 'OK' if 125 <= dl <= 150 else f'!!! desc={dl}'
        bad_t = []
        for i, t in enumerate(b['thoughts']):
            l = len(t['title']) + len(t['example'])
            if not (600 <= l <= 800):
                bad_t.append(f"{i+1}:{l}")
        tmark = 'thoughts OK' if not bad_t else f'thoughts BAD: {bad_t}'
        print(f"  {b['id']} {b['title']}: desc={dl} {dmark} | {tmark}")

if all_ok:
    with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, separators=(',', ':'))
    print("\nСохранено.")
else:
    print("\nЕСТЬ ОШИБКИ")
