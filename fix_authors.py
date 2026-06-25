import json

with open('/root/books/webapp/books.json', encoding='utf-8') as f:
    books = json.load(f)

professions = {
    930: "Рэпер, музыкант",
    931: "Певица, автор песен",
    932: "Актёр, философ, мастер боевых искусств",
    933: "Художник, сюрреалист",
    934: "Композитор",
    935: "Актёр, режиссёр",
    936: "Художница",
    937: "44-й президент США",
    938: "Певица, актриса",
    939: "Дизайнер, модельер"
}

for b in books:
    if b['id'] in professions:
        b['author'] = professions[b['id']]

with open('/root/books/webapp/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, separators=(',', ':'))

print('OK')
for b in books:
    if b['id'] in professions:
        print(b['id'], b['title'], '->', b['author'])
