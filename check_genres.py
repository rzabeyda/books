import json

books = json.load(open('/root/books/webapp/books.json'))
skip = {'цитаты', 'история успеха', 'блогеры', 'биографии'}

by_genre = {}
for b in books:
    if b['genre'] in skip:
        continue
    g = b['genre']
    if g not in by_genre:
        by_genre[g] = []
    by_genre[g].append((b['id'], b['title']))

for genre in sorted(by_genre):
    print(f"\n=== {genre} ===")
    for bid, title in by_genre[genre]:
        print(f"  {bid:3} | {title}")
