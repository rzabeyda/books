import json
with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

r3 = {
    (574,3): ' Именно поэтому место насилия стало местом роста.',
    (574,7): ' Тело не лжёт когда слов нет.',
    (574,9): ' Восемь лет — это не упорство. Это призвание.',
    (582,3): ' Медленное мышление строит — быстрое реагирует.',
    (582,5): ' Коппола не доверял себе — и снял шедевр.',
    (582,6): ' Омерта работает потому что это не правило — это идентичность.',
    (582,7): ' Стиль лидерства определяет судьбу организации.',
    (582,8): ' Хеллс-Китчен дал роману подлинность.',
    (582,9): ' Пьюзо описал власть без иллюзий.',
    (622,3): ' Река — учитель которого нельзя заменить текстом.',
    (622,5): ' Невыразимое опыт — честнее любого объяснения.',
}

for book in data:
    bid = book['id']
    for i, t in enumerate(book['thoughts']):
        if (bid, i) in r3:
            t['example'] = t['example'] + r3[(bid, i)]

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

ids = [574,582,622]
for book in data:
    if book['id'] in ids:
        lens = [len(t['example']) for t in book['thoughts']]
        bad = [(i,l) for i,l in enumerate(lens) if l < 700 or l > 820]
        status = 'OK' if not bad else f'BAD={bad}'
        print(f'ID={book["id"]:3d}: min={min(lens)} max={max(lens)} {status}')
