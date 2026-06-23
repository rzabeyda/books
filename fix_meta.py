import json

with open('/root/books/webapp/books.json', encoding='utf-8') as f:
    books = json.load(f)

meta = {
    849: {"author": "Пророк Мухаммад",        "year": "632"},
    850: {"author": "Наполеон Бонапарт",       "year": "1804"},
    851: {"author": "Франц Иосиф I",           "year": "1867"},
    852: {"author": "Фараон Нармер (Менес)",   "year": "3100 до н.э."},
    853: {"author": "Царица Дидона (Элисса)",  "year": "814 до н.э."},
    854: {"author": "Сигизмунд II Август",     "year": "1569"},
    855: {"author": "Мэйдзи (Муцухито)",       "year": "1868"},
}

for book in books:
    if book['id'] in meta:
        book['author'] = meta[book['id']]['author']
        book['year'] = meta[book['id']]['year']
        print(f"{book['id']}: author={book['author']}, year={book['year']}")

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

print("Done!")
