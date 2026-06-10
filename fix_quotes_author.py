import json

occupations = {
    155: 'Физик-теоретик',
    156: 'Премьер-министр Великобритании',
    157: 'Писатель',
    158: 'Политический лидер Индии',
    159: 'Писатель и поэт',
    160: 'Философ',
    161: 'Римский император и философ',
    162: 'Основатель Apple',
    163: 'Президент ЮАР',
    164: 'Философ Древнего Китая',
    165: 'Революционер и политик',
    166: 'Руководитель СССР',
    167: 'Руководитель КНР',
}

books = json.load(open('/root/books/webapp/books.json'))
for b in books:
    if b['id'] in occupations:
        b['author'] = occupations[b['id']]
        print(f"{b['title']} → {b['author']}")

json.dump(books, open('/root/books/webapp/books.json', 'w'), ensure_ascii=False, indent=2)
print('done')
