import json
with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

r2 = {
    (418,1): ' Дело урегулировано за $25 млн в 2008 году.',
    (418,9): ' Meta: $134 млрд выручки (2023), прибыль $39 млрд. Акции выросли в 3 раза за 2023 год.',
    (419,0): ' Кум вырос в бедности в Украине, эмигрировал в 16 лет, жил на пособие. Яблоки из еды банка помогли семье выжить.',
    (420,7): ' Одноклассники купило Mail.ru в 2010 году. Синергия: разная аудитория одной компании. ВКонтакте — молодёжь.',
    (422,8): ' LinkedIn Recruiter AI помогает подбирать кандидатов автоматически. LinkedIn создаёт инструменты которые угрожают профессии рекрутера.',
    (424,8): ' Условия труда в Amazon — постоянная тема. Безос ответил принципами: Amazon должен быть лучшим работодателем в мире. Слова и дела пока расходятся.',
}

for book in data:
    bid = book['id']
    for i, t in enumerate(book['thoughts']):
        if (bid, i) in r2:
            t['example'] = t['example'] + r2[(bid, i)]

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

ids = [418, 419, 420, 422, 424]
for book in data:
    if book['id'] in ids:
        dlens = len(book['description'])
        tlens = [len(t['example']) for t in book['thoughts']]
        t_bad = [(i,l) for i,l in enumerate(tlens) if l < 700 or l > 820]
        d_ok = 125 <= dlens <= 150
        status = 'OK' if d_ok and not t_bad else f'BAD desc={dlens} t={t_bad}'
        print(f'ID={book["id"]:3d} {book["title"][:20]:20s}: {status}')
