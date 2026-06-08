import re

# ── 1. index.html ──────────────────────────────────────────────
with open('/root/books/webapp/index.html', encoding='utf-8') as f:
    html = f.read()

print('=== HTML diagnostic ===')
print('has genre-pills-row:', 'genre-pills-row' in html)
print('has genre-btn:', 'genre-btn' in html)

# Убрать genre-pills-row
if 'genre-pills-row' in html:
    # пробуем несколько вариантов пробелов/переносов
    for variant in [
        '      <div class="genre-pills-row" id="genre-pills-row"></div>\n\n',
        '      <div class="genre-pills-row" id="genre-pills-row"></div>\n',
        '<div class="genre-pills-row" id="genre-pills-row"></div>',
    ]:
        if variant in html:
            html = html.replace(variant, '', 1)
            print('index.html: genre-pills-row убран (variant matched)')
            break
    else:
        print('index.html: WARNING - genre-pills-row не совпал ни с одним вариантом')

# Вернуть genre-btn если его нет
if 'genre-btn' not in html:
    genre_btn_html = '''          <button class="ctrl-btn ctrl-genre" id="genre-btn" onclick="openSheet('genre')">
            <span id="genre-label">Все книги</span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M6 9l6 6 6-6"/></svg>
          </button>
'''
    # ищем ctrl-reset чтобы вставить перед ним
    anchor = '          <button class="ctrl-btn ctrl-reset" id="reset-filters-btn"'
    if anchor in html:
        html = html.replace(anchor, genre_btn_html + anchor, 1)
        print('index.html: genre-btn восстановлен')
    else:
        print('index.html: WARNING - якорь для genre-btn не найден')
else:
    print('index.html: genre-btn уже есть')

with open('/root/books/webapp/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# ── 2. app.js ──────────────────────────────────────────────────
with open('/root/books/webapp/app.js', encoding='utf-8') as f:
    js = f.read()

print('\n=== JS diagnostic ===')
print('has renderGenrePills:', 'renderGenrePills' in js)
print('has genre-label in applyGenre:', 'genre-label' in js)

changed = False

# Убрать renderGenrePills() вызов из buildGenreOptions и саму функцию
if 'renderGenrePills' in js:
    old_build = "  GENRE_OPTIONS = [{ key: 'all', label: 'Все книги' }].concat(GENRES);\n  renderGenrePills();\n}\n\nfunction renderGenrePills() {\n  var row = document.getElementById('genre-pills-row');\n  if (!row) return;\n  row.innerHTML = GENRE_OPTIONS.map(function(o) {\n    var active = o.key === activeGenre;\n    return '<button class=\"genre-pill' + (active ? ' active' : '') + '\" onclick=\"applyGenre(\\'' + o.key + '\\')\">>' + o.label + '</button>';\n  }).join('');\n}"
    new_build = "  GENRE_OPTIONS = [{ key: 'all', label: 'Все книги' }].concat(GENRES);\n}"

    if old_build in js:
        js = js.replace(old_build, new_build, 1)
        print('app.js: renderGenrePills убран (exact)')
        changed = True
    else:
        # Попробуем regex подход — убрать всё что касается renderGenrePills
        # 1) вызов из buildGenreOptions
        js = re.sub(r'\n  renderGenrePills\(\);\n\}(\n\nfunction renderGenrePills.*?\})', '\n}', js, flags=re.DOTALL)
        print('app.js: renderGenrePills убран (regex)')
        changed = True

# Восстановить applyGenre с genre-label
old_apply_broken = '''function applyGenre(key) {
  activeGenre = key;
  closeSheet();
  renderGenrePills();
  renderList(filterByGenre(allBooks, activeGenre));
  updateResetBtn();
}'''
new_apply = '''function applyGenre(key) {
  activeGenre = key;
  var opt = GENRE_OPTIONS.find(function(o){ return o.key === key; }) || GENRE_OPTIONS[0];
  var lbl = document.getElementById('genre-label');
  if (lbl) lbl.textContent = opt ? opt.label : 'Все книги';
  closeSheet();
  renderList(filterByGenre(allBooks, activeGenre));
  updateResetBtn();
}'''
if old_apply_broken in js:
    js = js.replace(old_apply_broken, new_apply, 1)
    print('app.js: applyGenre восстановлен')
    changed = True
elif 'genre-label' in js:
    print('app.js: applyGenre уже содержит genre-label, пропускаем')
else:
    print('app.js: WARNING - applyGenre broken не найден')

# Восстановить resetFilters: убрать renderGenrePills(), добавить genre-label
old_reset_broken = "  document.getElementById('sort-label').textContent = 'Тираж';\n  updateResetBtn();\n  renderGenrePills();\n  renderList(filterByGenre(allBooks, 'all'));"
new_reset = "  document.getElementById('sort-label').textContent = 'Тираж';\n  var lbl2 = document.getElementById('genre-label');\n  if (lbl2) lbl2.textContent = 'Все книги';\n  updateResetBtn();\n  renderList(filterByGenre(allBooks, 'all'));"
if old_reset_broken in js:
    js = js.replace(old_reset_broken, new_reset, 1)
    print('app.js: resetFilters восстановлен')
    changed = True
elif "renderGenrePills" not in js:
    print('app.js: resetFilters уже ок (нет renderGenrePills)')
else:
    print('app.js: WARNING - resetFilters broken не найден')

if changed:
    with open('/root/books/webapp/app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print('app.js: сохранён')

# ── 3. style.css ──────────────────────────────────────────────
with open('/root/books/webapp/style.css', encoding='utf-8') as f:
    css = f.read()

print('\n=== CSS diagnostic ===')
print('has genre-pills-row:', 'genre-pills-row' in css)
print('has clickable-genre:', 'clickable-genre' in css)

if 'genre-pills-row' in css:
    # Убрать блок genre pills (от комментария до конца или до следующего блока)
    # Сначала найдём где начинается блок
    marker = '/* ── Genre pills'
    if marker in css:
        idx = css.index(marker)
        # Отрезаем от маркера до конца файла (блок обычно последний)
        css = css[:idx].rstrip() + '\n'
        print('style.css: genre-pills блок убран')
    else:
        # попробуем убрать отдельные правила
        css = re.sub(r'\.genre-pills-row\s*\{[^}]*\}', '', css)
        css = re.sub(r'\.genre-pills-row::-webkit-scrollbar\s*\{[^}]*\}', '', css)
        css = re.sub(r'\.genre-pill(?:\.active)?\s*\{[^}]*\}', '', css)
        print('style.css: genre-pills убраны через regex')

    with open('/root/books/webapp/style.css', 'w', encoding='utf-8') as f:
        f.write(css)

# ── 4. Убедиться что genre-sheet можно скроллить ──────────────
with open('/root/books/webapp/style.css', encoding='utf-8') as f:
    css = f.read()

if 'sheet-list' in css and 'overflow-y' not in css.split('sheet-list')[1].split('}')[0]:
    # Добавить overflow-y к .sheet-list
    css = css.replace('.sheet-list {', '.sheet-list {\n  overflow-y: auto;\n  max-height: 55vh;', 1)
    with open('/root/books/webapp/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('style.css: sheet-list overflow-y добавлен')
else:
    print('style.css: sheet-list уже ок или не найден')

print('\nDONE')
