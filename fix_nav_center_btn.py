

# --- index.html: add center button ---
with open('/root/books/webapp/index.html', 'r') as f:
    html = f.read()

old_header = '''        <button class="back-btn" onclick="prevBook()">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </button>
        <button class="next-btn" id="next-btn" onclick="nextBook()">'''

new_header = '''        <button class="back-btn" onclick="prevBook()">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </button>
        <button class="home-btn" onclick="goBackToList()">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/>
            <rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>
          </svg>
        </button>
        <button class="next-btn" id="next-btn" onclick="nextBook()">'''

if old_header in html:
    html = html.replace(old_header, new_header)
    print('OK: center button added to HTML')
else:
    print('ERROR: header pattern not found')

with open('/root/books/webapp/index.html', 'w') as f:
    f.write(html)

# --- app.js ---
with open('/root/books/webapp/app.js', 'r') as f:
    js = f.read()

# 1. Add scroll position variable after first var
old_var = 'var activeGenre = \'all\';'
new_var = 'var activeGenre = \'all\';\nvar listScrollPos = 0;'
if old_var in js:
    js = js.replace(old_var, new_var, 1)
    print('OK: listScrollPos variable added')
else:
    print('ERROR: activeGenre var not found')

# 2. Save scroll pos at the start of openBook
old_open = 'function openBook(id) {\n  var b = allBooks.filter(function(x) { return x.id === id; })[0];\n  if (!b) return;'
new_open = 'function openBook(id) {\n  var b = allBooks.filter(function(x) { return x.id === id; })[0];\n  if (!b) return;\n  listScrollPos = document.getElementById(\'screen-list\').scrollTop;'
if old_open in js:
    js = js.replace(old_open, new_open, 1)
    print('OK: scroll save added to openBook')
else:
    print('ERROR: openBook pattern not found')

# 3. Add goBackToList function after goHome
old_gohome = 'function goHome() {'
new_gohome = '''function goBackToList() {
  goHome();
  setTimeout(function() {
    document.getElementById('screen-list').scrollTop = listScrollPos;
  }, 0);
}

function goHome() {'''
if old_gohome in js:
    js = js.replace(old_gohome, new_gohome, 1)
    print('OK: goBackToList function added')
else:
    print('ERROR: goHome not found')

with open('/root/books/webapp/app.js', 'w') as f:
    f.write(js)

# --- style.css: style center button ---
with open('/root/books/webapp/style.css', 'r') as f:
    css = f.read()

old_css = '.back-btn {'
new_css = '''.home-btn {
  background: none;
  border: none;
  color: #aaa;
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.home-btn svg {
  width: 22px;
  height: 22px;
}
.home-btn:active { color: #f0c040; }

.back-btn {'''

if old_css in css:
    css = css.replace(old_css, new_css, 1)
    print('OK: home-btn style added')
else:
    print('ERROR: .back-btn not found in CSS')

with open('/root/books/webapp/style.css', 'w') as f:
    f.write(css)

print('Done.')
