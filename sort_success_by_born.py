import json

def born_sort_key(b):
    born = b.get('born', '')
    if not born:
        return 9999
    # Take first date before " — "
    date = born.split(' — ')[0].strip()
    parts = date.split('.')
    if len(parts) == 3:
        try:
            return int(parts[2]) * 10000 + int(parts[1]) * 100 + int(parts[0])
        except:
            pass
    return 9999

with open('/root/books/webapp/books.json') as f:
    books = json.load(f)

success = [b for b in books if b.get('genre') == 'история успеха']
other = [b for b in books if b.get('genre') != 'история успеха']

success_sorted = sorted(success, key=born_sort_key)

books_new = other + success_sorted

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(books_new, f, ensure_ascii=False, indent=2)

print('Sorted история успеха by born:')
for b in success_sorted:
    print(' ', b.get('born','—'), '|', b['title'])
