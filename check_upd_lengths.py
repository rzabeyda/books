with open('upd_books_995.py', 'r', encoding='utf-8') as f:
    content = f.read()

exec_globals = {}
exec(content.split('with open')[0], exec_globals)
updates = exec_globals['updates']

all_ok = True
for book_id, thoughts in updates.items():
    print(f'=== ID {book_id} ===')
    for i, t in enumerate(thoughts):
        length = len(t['title']) + len(t['example'])
        status = 'OK' if 600 <= length <= 800 else 'FAIL'
        if status == 'FAIL':
            all_ok = False
        print(f'  [{status}] {i+1}. {length}: {t["title"][:45]}')

print(f'\n{"ALL OK" if all_ok else "ЕСТЬ ОШИБКИ"}')
