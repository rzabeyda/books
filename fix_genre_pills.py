import re

# ── 1. index.html ──────────────────────────────────────────────
with open('/root/books/webapp/index.html', encoding='utf-8') as f:
    html = f.read()

# Убираем genre-btn
old_genre_btn = '''          <button class="ctrl-btn ctrl-genre" id="genre-btn" onclick="openSheet('genre')">
            <span id="genre-label">Все книги</span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M6 9l6 6 6-6"/></svg>
          </button>'''
new_genre_btn = ''

# Добавляем genre-pills-row после закрывающего тега top-bar
old_after_topbar = '      <div class="sheet-overlay" id="sheet-overlay" onclick="closeSheet()">'
new_after_topbar = '''      <div class="genre-pills-row" id="genre-pills-row"></div>

      <div class="sheet-overlay" id="sheet-overlay" onclick="closeSheet()">'''

if 'genre-pills-row' in html:
    print('index.html: уже исправлено')
else:
    if old_genre_btn in html:
        html = html.replace(old_genre_btn, new_genre_btn, 1)
        print('index.html: genre-btn убран')
    else:
        print('index.html: genre-btn NOT FOUND')
    if old_after_topbar in html:
        html = html.replace(old_after_topbar, new_after_topbar, 1)
        print('index.html: genre-pills-row добавлен')
    else:
        print('index.html: topbar anchor NOT FOUND')
    with open('/root/books/webapp/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

# ── 2. app.js ──────────────────────────────────────────────────
with open('/root/books/webapp/app.js', encoding='utf-8') as f:
    js = f.read()

if 'renderGenrePills' in js:
    print('app.js: уже исправлено')
else:
    # buildGenreOptions — добавляем вызов renderGenrePills
    old_build = '''  GENRE_OPTIONS = [{ key: 'all', label: 'Все книги' }].concat(GENRES);
}'''
    new_build = '''  GENRE_OPTIONS = [{ key: 'all', label: 'Все книги' }].concat(GENRES);
  renderGenrePills();
}

function renderGenrePills() {
  var row = document.getElementById('genre-pills-row');
  if (!row) return;
  row.innerHTML = GENRE_OPTIONS.map(function(o) {
    var active = o.key === activeGenre;
    return '<button class="genre-pill' + (active ? ' active' : '') + '" onclick="applyGenre(\\'' + o.key + '\\')">' + o.label + '</button>';
  }).join('');
}'''
    if old_build in js:
        js = js.replace(old_build, new_build, 1)
        print('app.js: buildGenreOptions + renderGenrePills OK')
    else:
        print('app.js: buildGenreOptions NOT FOUND')

    # applyGenre — убираем genre-label, добавляем renderGenrePills
    old_apply = '''function applyGenre(key) {
  activeGenre = key;
  var opt = GENRE_OPTIONS.find(function(o){ return o.key === key; });
  document.getElementById('genre-label').textContent = opt.label;
  closeSheet();
  renderList(filterByGenre(allBooks, activeGenre));
  updateResetBtn();
}'''
    new_apply = '''function applyGenre(key) {
  activeGenre = key;
  closeSheet();
  renderGenrePills();
  renderList(filterByGenre(allBooks, activeGenre));
  updateResetBtn();
}'''
    if old_apply in js:
        js = js.replace(old_apply, new_apply, 1)
        print('app.js: applyGenre OK')
    else:
        print('app.js: applyGenre NOT FOUND')

    # resetFilters — убираем genre-label, добавляем renderGenrePills
    old_reset = '''  document.getElementById('sort-label').textContent = 'Тираж';
  document.getElementById('genre-label').textContent = 'Все книги';
  updateResetBtn();
  renderList(filterByGenre(allBooks, 'all'));'''
    new_reset = '''  document.getElementById('sort-label').textContent = 'Тираж';
  updateResetBtn();
  renderGenrePills();
  renderList(filterByGenre(allBooks, 'all'));'''
    if old_reset in js:
        js = js.replace(old_reset, new_reset, 1)
        print('app.js: resetFilters OK')
    else:
        print('app.js: resetFilters NOT FOUND')

    with open('/root/books/webapp/app.js', 'w', encoding='utf-8') as f:
        f.write(js)

# ── 3. style.css ──────────────────────────────────────────────
with open('/root/books/webapp/style.css', encoding='utf-8') as f:
    css = f.read()

if 'genre-pills-row' in css:
    print('style.css: уже есть')
else:
    css += '''
/* ── Genre pills ────────────────────────────── */
.genre-pills-row {
  display: flex;
  overflow-x: auto;
  gap: 8px;
  padding: 8px 12px 10px;
  scrollbar-width: none;
  -ms-overflow-style: none;
  background: #111;
  border-bottom: 1px solid #1e1e1e;
  flex-shrink: 0;
}
.genre-pills-row::-webkit-scrollbar { display: none; }
.genre-pill {
  flex-shrink: 0;
  background: #1e1e1e;
  color: #aaa;
  border: 1px solid #2a2a2a;
  border-radius: 20px;
  padding: 5px 14px;
  font-size: 13px;
  cursor: pointer;
  white-space: nowrap;
  font-family: inherit;
  transition: background 0.15s, color 0.15s;
}
.genre-pill.active {
  background: #f0c040;
  color: #111;
  font-weight: 600;
  border-color: #f0c040;
}
'''
    with open('/root/books/webapp/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('style.css: OK')
