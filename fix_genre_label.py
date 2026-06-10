content = open('/root/books/webapp/app.js').read()
old = "'священные писания': 'Священные писания',"
new = "'священные писания': 'Священные писания',\n  'художественная':    'Художественная',"
content = content.replace(old, new)
open('/root/books/webapp/app.js', 'w').write(content)
print('done')
