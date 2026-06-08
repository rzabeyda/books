with open('/root/books/webapp/app.js', encoding='utf-8') as f:
    js = f.read()

old_fn = """function buildGenreOptions() {
  var maxId = {};
  allBooks.forEach(function(b) {
    if (b.genre && (!maxId[b.genre] || b.id > maxId[b.genre])) maxId[b.genre] = b.id;
  });
  var sorted = Object.keys(maxId).sort(function(a, b) { return maxId[b] - maxId[a]; });
  GENRES = sorted.map(function(k) { return { key: k, label: GENRE_LABELS[k] || k }; });
  GENRE_OPTIONS = [{ key: 'all', label: 'Все книги' }].concat(GENRES);
}"""

new_fn = """function buildGenreOptions() {
  var cnt = {};
  allBooks.forEach(function(b) {
    if (b.genre) cnt[b.genre] = (cnt[b.genre] || 0) + 1;
  });
  var sorted = Object.keys(cnt).sort(function(a, b) { return cnt[b] - cnt[a]; });
  GENRES = sorted.map(function(k) { return { key: k, label: GENRE_LABELS[k] || k }; });
  GENRE_OPTIONS = [{ key: 'all', label: 'Все книги' }].concat(GENRES);
}"""

js = js.replace(old_fn, new_fn, 1)

# bump version
with open('/root/books/webapp/index.html', encoding='utf-8') as f:
    html = f.read()
html = html.replace('app.js?v=32', 'app.js?v=33')
with open('/root/books/webapp/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('/root/books/webapp/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print('done v33 — genre sort by count')
