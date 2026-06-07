
# --- index.html: replace SVG with text "Книги" ---
with open('/root/books/webapp/index.html', 'r') as f:
    html = f.read()

old_btn = '''        <button class="home-btn" onclick="goBackToList()">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/>
            <rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>
          </svg>
        </button>'''

new_btn = '        <button class="home-btn" onclick="goBackToList()">Книги</button>'

if old_btn in html:
    html = html.replace(old_btn, new_btn)
    print('OK: SVG replaced with Книги text')
else:
    print('ERROR: home-btn SVG not found')

with open('/root/books/webapp/index.html', 'w') as f:
    f.write(html)

# --- style.css: layout fixes ---
with open('/root/books/webapp/style.css', 'r') as f:
    css = f.read()

# detail-header: space-between instead of gap
old_header = '.detail-header { height: 56px; display: flex; align-items: center; gap: 10px; padding: 0 14px; border-bottom: 1px solid #1c1c1c; flex-shrink: 0; }'
new_header = '.detail-header { height: 56px; display: flex; align-items: center; justify-content: space-between; padding: 0 14px; border-bottom: 1px solid #1c1c1c; flex-shrink: 0; }'
if old_header in css:
    css = css.replace(old_header, new_header)
    print('OK: detail-header layout updated')
else:
    print('ERROR: detail-header not found')

# home-btn: text button style like back/next
old_home = '''.home-btn {
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
.home-btn:active { color: #f0c040; }'''

new_home = '.home-btn { background: var(--bg3); border: none; border-radius: 12px; padding: 8px 16px; font-size: 13px; font-weight: 600; color: var(--text); cursor: pointer; transition: background .15s, color .15s; flex-shrink: 0; }\n.home-btn:active { background: #3a3a3a; color: var(--accent); }'

if old_home in css:
    css = css.replace(old_home, new_home)
    print('OK: home-btn style updated')
else:
    print('ERROR: home-btn style not found')

with open('/root/books/webapp/style.css', 'w') as f:
    f.write(css)

print('Done.')
