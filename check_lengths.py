with open('add_books_990.py', 'r', encoding='utf-8') as f:
    content = f.read()

exec_globals = {}
exec(content.split('with open')[0], exec_globals)
new_books = exec_globals['new_books']

for book in new_books:
    title = book['title']
    print(f'=== {title} ===')
    for i, t in enumerate(book['thoughts']):
        length = len(t['title']) + len(t['example'])
        status = 'OK' if 600 <= length <= 800 else 'FAIL'
        print(f'  [{status}] {i+1}. {length}: {t["title"][:45]}')
