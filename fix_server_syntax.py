content = open('/root/books/server.py').read()

# Fix broken string literal with literal newline
content = content.replace(
    "msg = '📚 Предложение книги:\n' + text",
    "msg = '📚 Предложение книги:\\n' + text"
)

open('/root/books/server.py', 'w').write(content)
print('Fixed')
