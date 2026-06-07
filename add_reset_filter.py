
# Добавляем кнопку сброса фильтров

# --- index.html ---
with open('/root/books/webapp/index.html', 'r') as f:
    html = f.read()

old_html = '          <button class="ctrl-btn ctrl-genre" id="genre-btn" onclick="openSheet(\'genre\')">'
new_html = ('          <button class="ctrl-btn ctrl-reset" id="reset-filters-btn" onclick="resetFilters()" style="display:none" title="Сбросить фильтры">'
            '<svg viewBox="0 0 20 20" width="18" height="18"><circle cx="10" cy="10" r="10" fill="#e53935"/>'
            '<line x1="6" y1="6" x2="14" y2="14" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>'
            '<line x1="14" y1="6" x2="6" y2="14" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>'
            '</svg></button>\n'
            '          <button class="ctrl-btn ctrl-genre" id="genre-btn" onclick="openSheet(\'genre\')">')

if old_html in html:
    html = html.replace(old_html, new_html, 1)
    print('OK: кнопка сброса добавлена в index.html')
else:
    print('ERROR: pattern not found in index.html')

with open('/root/books/webapp/index.html', 'w') as f:
    f.write(html)

# --- app.js ---
with open('/root/books/webapp/app.js', 'r') as f:
    js = f.read()

# Добавляем функцию resetFilters и updateResetBtn после объявления activeSort
old_vars = 'var activeSort = \'sales\';'
new_vars = ('var activeSort = \'sales\';\n'
            'function updateResetBtn() {\n'
            '  var btn = document.getElementById(\'reset-filters-btn\');\n'
            '  if (!btn) return;\n'
            '  btn.style.display = (activeSort !== \'sales\' || activeGenre !== \'all\') ? \'flex\' : \'none\';\n'
            '}\n'
            'function resetFilters() {\n'
            '  activeSort = \'sales\';\n'
            '  activeGenre = \'all\';\n'
            '  document.getElementById(\'sort-label\').textContent = \'По продажам\';\n'
            '  document.getElementById(\'genre-label\').textContent = \'Все книги\';\n'
            '  updateResetBtn();\n'
            '  renderList(filterByGenre(allBooks, \'all\'));\n'
            '}')

if old_vars in js:
    js = js.replace(old_vars, new_vars, 1)
    print('OK: функции resetFilters/updateResetBtn добавлены')
else:
    print('ERROR: activeSort var not found')

# Вызываем updateResetBtn() в applySort после renderList
old_apply_sort = ('  renderList(filterByGenre(allBooks, activeGenre));\n'
                  '}\n'
                  'function applyGenre')
new_apply_sort = ('  renderList(filterByGenre(allBooks, activeGenre));\n'
                  '  updateResetBtn();\n'
                  '}\n'
                  'function applyGenre')

if old_apply_sort in js:
    js = js.replace(old_apply_sort, new_apply_sort, 1)
    print('OK: updateResetBtn добавлен в applySort')
else:
    print('ERROR: applySort end not found')

# Вызываем updateResetBtn() в applyGenre после renderList
old_apply_genre = ('  renderList(filterByGenre(allBooks, activeGenre));\n'
                   '}\n'
                   'function closeSheet')
new_apply_genre = ('  renderList(filterByGenre(allBooks, activeGenre));\n'
                   '  updateResetBtn();\n'
                   '}\n'
                   'function closeSheet')

if old_apply_genre in js:
    js = js.replace(old_apply_genre, new_apply_genre, 1)
    print('OK: updateResetBtn добавлен в applyGenre')
else:
    print('ERROR: applyGenre end not found')

with open('/root/books/webapp/app.js', 'w') as f:
    f.write(js)

# --- style.css ---
with open('/root/books/webapp/style.css', 'r') as f:
    css = f.read()

reset_style = '\n.ctrl-reset { background: none; border: none; padding: 2px 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }\n'

if '.ctrl-reset' not in css:
    css += reset_style
    print('OK: стиль ctrl-reset добавлен')
else:
    print('стиль уже есть')

with open('/root/books/webapp/style.css', 'w') as f:
    f.write(css)

print('Done.')
