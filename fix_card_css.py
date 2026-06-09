content = open('/root/books/webapp/style.css').read()

old = '.sub-plan {'
new = 'a.sub-plan { text-decoration: none; }\n.sub-plan {'

content = content.replace(old, new, 1)
open('/root/books/webapp/style.css', 'w').write(content)
print('Done')
