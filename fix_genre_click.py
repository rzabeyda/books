import re

# --- app.js: section-label становится кликабельным ---
with open('/root/books/webapp/app.js', encoding='utf-8') as f:
    js = f.read()

old_js = "'<div class=\"section-label\">' + g.label + '</div>'"
new_js = "'<div class=\"section-label clickable-genre\" onclick=\"applyGenre(\\'' + g.key + '\\')\">' + g.label + '<span class=\"section-arrow\">→</span></div>'"

if 'clickable-genre' in js:
    print('app.js: уже исправлено')
elif old_js in js:
    js = js.replace(old_js, new_js, 1)
    with open('/root/books/webapp/app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print('app.js: OK')
else:
    print('app.js: NOT FOUND — ' + repr(old_js[:60]))

# --- style.css: добавить стили ---
with open('/root/books/webapp/style.css', encoding='utf-8') as f:
    css = f.read()

new_css = """
.clickable-genre {
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.clickable-genre:active {
  opacity: 0.6;
}
.section-arrow {
  font-size: 16px;
  color: #f0c040;
  opacity: 0.8;
}
"""

if 'clickable-genre' in css:
    print('style.css: уже есть')
else:
    css += new_css
    with open('/root/books/webapp/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('style.css: OK')
