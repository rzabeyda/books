with open('/root/books/webapp/app.js') as f:
    js = f.read()

idx = js.find('function showSubInfo')
end = js.find('\nfunction ', idx + 10)
old_func = js[idx:end]

new_func = """async function showSubInfo() {
  var text = document.getElementById('sub-info-text');
  var overlay = document.getElementById('sub-info-overlay');
  if (!text || !overlay) return;
  overlay.classList.add('show');
  text.innerHTML = 'Загрузка...';

  var expires = subExpiresDate || (localStorage.getItem('subExpires') ? new Date(localStorage.getItem('subExpires')) : null);

  if (!expires) {
    var uid = getTelegramUid();
    if (uid) {
      try {
        var resp = await fetch(API + '/subscription/' + uid);
        var data = await resp.json();
        if (data.expires) {
          expires = new Date(data.expires);
          subExpiresDate = expires;
          localStorage.setItem('subExpires', data.expires);
        }
      } catch(e) {}
    }
  }

  if (expires) {
    var days = getDaysLeft();
    var dateStr = expires.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
    var daysStr = days > 0 ? 'Осталось: <b>' + days + ' дн.</b>' : '<span style=color:#e53935>Истекла</span>';
    text.innerHTML = 'Активна до: <b>' + dateStr + '</b><br>' + daysStr;
  } else {
    text.innerHTML = '✅ Подписка активна';
  }
}
"""

js = js[:idx] + new_func + js[end:]
with open('/root/books/webapp/app.js', 'w') as f:
    f.write(js)

# bump version
with open('/root/books/webapp/index.html') as f:
    html = f.read()
html = html.replace('app.js?v=30', 'app.js?v=31')
with open('/root/books/webapp/index.html', 'w') as f:
    f.write(html)

print('done, v31')
