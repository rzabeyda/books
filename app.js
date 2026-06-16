var allBooks = [];
var API = 'https://books.zabeyda.lol';
var readBooks = new Set(JSON.parse(localStorage.getItem('readBooks') || '[]'));
var favoriteBooks = new Set(JSON.parse(localStorage.getItem('favoriteBooks') || '[]'));
var activeGenre = 'all';
var activeSort = 'sections';
var currentListForNav = [];
var allReactions = {};
var autoScrollStopped = false;

var SORT_OPTIONS = [
  { key: 'sections',    label: 'Разделы' },
  { key: 'newer',       label: 'Новое' },
  { key: 'sales',       label: 'Популярные' },
  { key: 'recommended', label: 'Рекомендованные' },
  { key: 'read',        label: 'Прочитанные' },
  { key: 'unread',      label: 'Не прочитанные' },
  { key: 'az',          label: 'По названию А → Я' },
  { key: 'za',          label: 'По названию Я → А' },
];

var GENRE_OPTIONS = [
  { key: 'all',               label: 'Все книги' },
  { key: 'от автора',         label: 'От автора' },
  { key: 'история успеха',    label: 'История успеха' },
  { key: 'биографии',         label: 'Биографии' },
  { key: 'саморазвитие',      label: 'Саморазвитие' },
  { key: 'психология',        label: 'Психология' },
  { key: 'блогеры',           label: 'Блогеры и стримеры' },
  { key: 'цитаты',            label: 'Цитаты' },
  { key: 'классика',          label: 'Классика' },
  { key: 'художественная',    label: 'Художественная' },
  { key: 'романы',             label: 'Романы' },
  { key: 'философия',         label: 'Философия' },
  { key: 'эзотерика',         label: 'Эзотерика' },
  { key: 'бизнес',            label: 'Бизнес' },
  { key: 'отношения',         label: 'Любовь / Отношения' },
  { key: 'семья',             label: 'Семья / Дети' },
  { key: 'здоровье',          label: 'Здоровье' },
  { key: 'детективы',         label: 'Детективы' },
  { key: 'фантастика',        label: 'Фантастика' },
  { key: 'мемуары',           label: 'Мемуары' },
  { key: 'история',           label: 'История' },
  { key: 'политика',          label: 'Политика' },
  { key: 'сказки',            label: 'Сказки и фэнтези' },
  { key: 'наука',             label: 'Наука' },
  { key: 'священные писания', label: 'Священные писания' },
  { key: 'игры',              label: 'Игры' },
  { key: 'империи',           label: 'Империи' },
  { key: 'история бренда',    label: 'История брендов' },
  { key: 'favorites',         label: 'Избранное' },
];

function buildRecommendWeights() {
  var genre = {}, author = {};
  allBooks.forEach(function(b) {
    if (!readBooks.has(b.id)) return;
    genre[b.genre]   = (genre[b.genre]   || 0) + 1;
    author[b.author] = (author[b.author] || 0) + 1;
  });
  return { genre: genre, author: author };
}

function recommendScore(b, weights) {
  if (readBooks.has(b.id)) return -1;
  return (weights.genre[b.genre] || 0) * 2 + (weights.author[b.author] || 0) * 3;
}

function sortBooks(books, sort) {
  var s = books.slice();
  if (sort === 'sections') return s.sort(function(a,b){
    var ra = readBooks.has(a.id) ? 1 : 0, rb = readBooks.has(b.id) ? 1 : 0;
    if (ra !== rb) return ra - rb;
    return (b.world_reads || 0) - (a.world_reads || 0);
  });
  if (sort === 'sales') {
    var skipGenres = ['история бренда', 'история успеха'];
    return s.sort(function(a,b){
      var ra = skipGenres.indexOf(a.genre) >= 0 ? -1 : (a.world_reads || 0);
      var rb = skipGenres.indexOf(b.genre) >= 0 ? -1 : (b.world_reads || 0);
      return rb - ra;
    });
  }
  if (sort === 'newer')    return s.sort(function(a,b){ return b.id - a.id; });
  if (sort === 'older')    return s.sort(function(a,b){ return (a.year||0) - (b.year||0); });
  if (sort === 'az')       return s.sort(function(a,b){ return a.title.localeCompare(b.title, 'ru'); });
  if (sort === 'za')       return s.sort(function(a,b){ return b.title.localeCompare(a.title, 'ru'); });
  if (sort === 'thoughts') return s.sort(function(a,b){ return b.thoughts.length - a.thoughts.length; });
  if (sort === 'author')   return s.sort(function(a,b){ return a.author.localeCompare(b.author, 'ru'); });
  if (sort === 'authorza') return s.sort(function(a,b){ return b.author.localeCompare(a.author, 'ru'); });
  if (sort === 'read')     return s.sort(function(a,b){ return (readBooks.has(b.id)?1:0) - (readBooks.has(a.id)?1:0); });
  if (sort === 'unread')   return s.sort(function(a,b){ return (readBooks.has(a.id)?1:0) - (readBooks.has(b.id)?1:0); });
  if (sort === 'recommended') {
    var w = buildRecommendWeights();
    return s.sort(function(a,b){ return recommendScore(b, w) - recommendScore(a, w); });
  }
  return s;
}

function openSheet(type) {
  var overlay = document.getElementById('sheet-overlay');
  var sheet   = document.getElementById('sheet');
  var title   = document.getElementById('sheet-title');
  var list    = document.getElementById('sheet-list');

  if (type === 'sort') {
    title.textContent = 'Сортировка';
    list.innerHTML = SORT_OPTIONS.map(function(o) {
      var active = o.key === activeSort;
      var countHtml = (o.key === 'read' || o.key === 'unread')
        ? '<span class="sheet-count">' + (o.key === 'read' ? readBooks.size : allBooks.length - readBooks.size) + '</span>'
        : '';
      return '<button class="sheet-item' + (active ? ' active' : '') + '" onclick="applySort(\'' + o.key + '\')">' +
        o.label + countHtml + (active ? '<span class="sheet-check">✓</span>' : '') + '</button>';
    }).join('');
  } else {
    title.textContent = 'Раздел';
    var genreWithCounts = GENRE_OPTIONS.map(function(o) {
      var count = o.key === 'all' ? allBooks.length : o.key === 'favorites' ? favoriteBooks.size : allBooks.filter(function(b){ return b.genre === o.key; }).length;
      return { o: o, count: count };
    });
    var allOpt = genreWithCounts.filter(function(x){ return x.o.key === 'all'; });
    var favOpt = genreWithCounts.filter(function(x){ return x.o.key === 'favorites'; });
    var rest = genreWithCounts.filter(function(x){ return x.o.key !== 'all' && x.o.key !== 'favorites'; })
      .sort(function(a, b){ return b.count - a.count; });
    list.innerHTML = allOpt.concat(rest).concat(favOpt).map(function(x) {
      var active = x.o.key === activeGenre;
      return '<button class="sheet-item' + (active ? ' active' : '') + '" onclick="applyGenre(\'' + x.o.key + '\')">' +
        x.o.label + '<span class="sheet-count">' + x.count + '</span>' + (active ? '<span class="sheet-check">✓</span>' : '') + '</button>';
    }).join('');
  }

  overlay.classList.add('show');
  sheet.classList.add('show');
  document.getElementById('scroll-top-btn').classList.remove('visible');
}

function closeSheet() {
  document.getElementById('sheet-overlay').classList.remove('show');
  document.getElementById('sheet').classList.remove('show');
}

function updateSortLabel() {
  var opt = SORT_OPTIONS.find(function(o){ return o.key === activeSort; });
  var label = opt.label;
  if (activeSort === 'read')   label = 'Прочитанные · ' + readBooks.size;
  if (activeSort === 'unread') label = 'Не прочитанные · ' + (allBooks.length - readBooks.size);
  document.getElementById('sort-label').textContent = label;
}

function applySort(key) {
  activeSort = key;
  updateSortLabel();
  closeSheet();
  renderList(filterByGenre(allBooks, activeGenre));
}

function resetFilters() {
  activeSort = 'sections';
  updateSortLabel();
  applyGenre('all');
}

function applyGenre(key) {
  activeGenre = key;
  var opt = GENRE_OPTIONS.find(function(o){ return o.key === key; });
  document.getElementById('genre-label').textContent = opt.label;
  closeSheet();
  renderList(filterByGenre(allBooks, activeGenre));
}

function openSearch() {
  setScreen('list');
  document.getElementById('genre-tabs').style.display = 'none';
  document.getElementById('search-bar').style.display = 'flex';
  var inp = document.getElementById('search-input');
  inp.value = '';
  setTimeout(function() { inp.focus(); }, 50);
}

function closeSearch() {
  document.getElementById('search-bar').style.display = 'none';
  document.getElementById('genre-tabs').style.display = 'flex';
  document.getElementById('search-input').value = '';
  renderList(filterByGenre(allBooks, activeGenre));
}

function saveReadBooks() {
  localStorage.setItem('readBooks', JSON.stringify([...readBooks]));
}

async function init() {
  var tg = window.Telegram && window.Telegram.WebApp;
  if (tg && tg.ready) tg.ready();
  try {
    var booksRes = await fetch(API + '/books.json?v=' + Date.now());
    allBooks = await booksRes.json();
    renderList(allBooks);
    var bookParam = new URLSearchParams(window.location.search).get('book');
    if (bookParam) openBook(parseInt(bookParam));
    if (document.getElementById('sheet').classList.contains('show')) openSheet('genre');
    checkSubscription();
    setTimeout(checkSubscription, 1500);
  } catch(e) {
    document.getElementById('books-list').innerHTML = '<div class="empty-state">Ошибка загрузки</div>';
  }
  try {
    var rRes = await fetch(API + '/reactions');
    allReactions = await rRes.json();
  } catch(e) {}

  document.getElementById('search-input').addEventListener('input', function(e) {
    var q = e.target.value.trim().toLowerCase();
    renderList(q ? allBooks.filter(function(b) {
      return b.title.toLowerCase().includes(q) || b.author.toLowerCase().includes(q);
    }) : filterByGenre(allBooks, activeGenre));
  });

}

function md(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>');
}

function coverImg(src, alt) {
  if (!src) return '';
  return '<img src="' + src + '?v=3" alt="' + alt + '" loading="lazy" onerror="this.style.display=\'none\'">';
}

function formatYear(y) {
  if (!y && y !== 0) return '';
  if (y < 0) return Math.abs(y) + 'г до н.э.';
  return y + 'г';
}

function filterByGenre(books, genre) {
  if (genre === 'all') return books;
  if (genre === 'favorites') return books.filter(function(b) { return favoriteBooks.has(b.id); });
  return books.filter(function(b) { return b.genre === genre; });
}

function saveFavoriteBooks() {
  localStorage.setItem('favoriteBooks', JSON.stringify([...favoriteBooks]));
}

function toggleFavorite(id) {
  if (favoriteBooks.has(id)) {
    favoriteBooks.delete(id);
  } else {
    favoriteBooks.add(id);
  }
  saveFavoriteBooks();
  var isFav = favoriteBooks.has(id);
  var btn = document.getElementById('fav-btn');
  if (btn) btn.textContent = isFav ? '❤️' : '🤍';
}

function shareBook(id) {
  var b = allBooks.filter(function(x) { return x.id === id; })[0];
  if (!b) return;
  var text = '📖 ' + b.title + (b.author ? ' — ' + b.author : '') + '\n\nЧитай главные мысли из этой книги 👇';
  var url = 'https://books.zabeyda.lol/?book=' + id;
  var shareUrl = 'https://t.me/share/url?url=' + encodeURIComponent(url) + '&text=' + encodeURIComponent(text);
  if (window.Telegram && Telegram.WebApp) {
    Telegram.WebApp.openTelegramLink(shareUrl);
  } else {
    window.open(shareUrl, '_blank');
  }
}

var GENRES = [
  { key: 'биографии',         label: 'Биографии' },
  { key: 'психология',        label: 'Психология' },
  { key: 'история успеха',    label: 'История успеха' },
  { key: 'саморазвитие',      label: 'Саморазвитие' },
  { key: 'блогеры',           label: 'Блогеры и стримеры' },
  { key: 'цитаты',            label: 'Цитаты' },
  { key: 'классика',          label: 'Классика' },
  { key: 'художественная',    label: 'Художественная' },
  { key: 'романы',             label: 'Романы' },
  { key: 'философия',         label: 'Философия' },
  { key: 'эзотерика',         label: 'Эзотерика' },
  { key: 'бизнес',            label: 'Бизнес' },
  { key: 'отношения',         label: 'Любовь / Отношения' },
  { key: 'семья',             label: 'Семья / Дети' },
  { key: 'здоровье',          label: 'Здоровье' },
  { key: 'детективы',         label: 'Детективы' },
  { key: 'фантастика',        label: 'Фантастика' },
  { key: 'мемуары',           label: 'Мемуары' },
  { key: 'история',           label: 'История' },
  { key: 'политика',          label: 'Политика' },
  { key: 'сказки',            label: 'Сказки и фэнтези' },
  { key: 'наука',             label: 'Наука' },
  { key: 'священные писания', label: 'Священные писания' },
  { key: 'игры',              label: 'Игры' },
  { key: 'империи',           label: 'Империи' },
  { key: 'история бренда',    label: 'История брендов' },
];

function topCardHtml(b, genreKey) {
  var isRead = readBooks.has(b.id);
  return '<div class="top-card' + (isRead ? ' read' : '') + '" onclick="openBook(' + b.id + ',\'' + genreKey + '\')">' +
    '<div class="top-img">' + coverImg(b.cover, b.title) + '</div>' +
    '<div class="top-card-title">' + b.title + '</div>' +
    '<div class="top-card-author">' + (b.platform || b.role || b.author) + '</div>' +
    (b.year ? '<div class="top-card-reads" style="color:#5b9cf6">' + formatYear(b.year) + '</div>' : '') +
    '</div>';
}

function renderList(books) {
  var sorted = sortBooks(books, activeSort);
  currentListForNav = sorted;

  var genreHtml = '';
  var searching = books.length !== allBooks.length;

  if (!searching && activeSort === 'sections') {
    var genresSorted = GENRES.map(function(g) {
      return { g: g, books: sorted.filter(function(b) { return b.genre === g.key; }) };
    }).filter(function(x) { return x.books.length > 0; })
      .sort(function(a, b) {
        return b.books.length - a.books.length;
      });

    genresSorted.forEach(function(x) {
      var sectionBooks = x.books.slice().sort(function(a,b){
        var ra = readBooks.has(a.id) ? 1 : 0, rb = readBooks.has(b.id) ? 1 : 0;
        if (ra !== rb) return ra - rb;
        return (b.world_reads || 0) - (a.world_reads || 0);
      });
      genreHtml +=
        '<div class="section-label" onclick="applyGenre(\'' + x.g.key + '\')" style="cursor:pointer">' + x.g.label + ' →</div>' +
        '<div class="top-scroll">' + sectionBooks.map(function(b){ return topCardHtml(b, x.g.key); }).join('') + '</div>';
    });
  }

  var gridHtml = sorted.map(function(b) {
    var isRead = readBooks.has(b.id);
    return '<div class="book-card' + (isRead ? ' read' : '') + '" onclick="openBook(' + b.id + ')">' +
      '<div class="grid-img">' + coverImg(b.cover, b.title) + '</div>' +
      '<div class="book-info">' +
      '<div class="book-title">' + b.title + '</div>' +
      '<div class="book-author">' + (b.platform || b.role || b.author) + '</div>' +
      (b.year ? '<div class="book-reads" style="color:#5b9cf6">' + formatYear(b.year) + '</div>' : '') +
      '</div></div>';
  }).join('');

  var resetEl = document.getElementById('genre-reset-btn');
  if (resetEl) resetEl.style.display = (activeGenre !== 'all' || activeSort !== 'sections') ? 'flex' : 'none';

  document.getElementById('books-list').innerHTML =
    genreHtml +
    '<div class="books-grid">' + (gridHtml || '<div class="empty-state">Ничего не найдено</div>') + '</div>' +
    '<div class="suggest-book-btn" onclick="openSuggestModal()">📚 Предложить книгу</div>';

  if (!searching && activeSort !== 'newer') {
    setTimeout(function() {
      var els = document.querySelectorAll('.top-scroll');
      if (!els.length) return;
      els.forEach(function(el) {
        function tick() {
          if (autoScrollStopped) return;
          el.scrollLeft += 0.45;
          if (el.scrollLeft >= el.scrollWidth - el.offsetWidth) {
            el.scrollLeft = 0;
          }
          requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      });
    }, 500);
  }
}

function openSuggestModal() {
  document.getElementById('suggest-modal').style.display = 'flex';
  document.getElementById('suggest-title').value = '';
  document.getElementById('suggest-author').value = '';
  document.getElementById('suggest-title').focus();
}

function closeSuggestModal() {
  document.getElementById('suggest-modal').style.display = 'none';
}

function submitSuggest() {
  var title = document.getElementById('suggest-title').value.trim();
  var author = document.getElementById('suggest-author').value.trim();
  if (!title) { document.getElementById('suggest-title').focus(); return; }

  var user = window.Telegram && Telegram.WebApp && Telegram.WebApp.initDataUnsafe && Telegram.WebApp.initDataUnsafe.user;
  var userName = user ? (user.first_name + (user.last_name ? ' ' + user.last_name : '') + (user.username ? ' @' + user.username : '')) : 'Аноним';

  var text = '📚 Запрос на книгу\n\nКнига: ' + title + (author ? '\nАвтор: ' + author : '') + '\nОт: ' + userName;

  fetch(API + '/suggest', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: text })
  }).then(function() {
    document.getElementById('suggest-modal').style.display = 'none';
    showSuggestToast();
  }).catch(function() {
    document.getElementById('suggest-modal').style.display = 'none';
    showSuggestToast();
  });
}

function showSuggestToast() {
  var toast = document.getElementById('suggest-toast');
  toast.style.display = 'block';
  setTimeout(function() { toast.style.display = 'none'; }, 3000);
}

function openBook(id, genreKey) {
  autoScrollStopped = true;
  var b = allBooks.filter(function(x) { return x.id === id; })[0];
  if (!b) return;
  if (genreKey) {
    activeGenre = genreKey;
    currentListForNav = filterByGenre(allBooks, genreKey);
  }

  var titleEl = document.getElementById('detail-title-top');
  if (titleEl) titleEl.textContent = b.title;
  document.getElementById('next-btn').dataset.currentId = b.id;

  var isSubbed = !!localStorage.getItem('sub_expires');
  var FREE_BOOKS = 10;
  var freeUsed = JSON.parse(localStorage.getItem('free_books') || '[]');
  var bookIdStr = String(b.id);
  var alreadyFree = freeUsed.indexOf(bookIdStr) !== -1;
  var canRead = isSubbed || alreadyFree || freeUsed.length < FREE_BOOKS;

  if (!alreadyFree && !isSubbed && freeUsed.length < FREE_BOOKS) {
    freeUsed.push(bookIdStr);
    localStorage.setItem('free_books', JSON.stringify(freeUsed));
  }

  var thoughtsHtml = b.thoughts.map(function(t, i) {
    if (!canRead) return '';
    return '<div class="thought-card">' +
      '<div class="thought-num">№' + (i + 1) + '</div>' +
      '<div class="thought-title">' + t.title + '</div>' +
      '<div class="thought-example">' + md(t.example) + '</div>' +
      (t.life ? '<div class="thought-life"><span class="thought-tag">В жизни:</span> ' + md(t.life) + '</div>' : '') +
      (t.question ? '<div class="thought-question"><span class="thought-tag">Вопрос себе:</span> ' + t.question + '</div>' : '') +
      '</div>';
  }).join('');

  if (!canRead) {
    thoughtsHtml = '<div class="paywall-block" onclick="openSub()">' +
      '<div class="paywall-lock">🔒</div>' +
      '<div class="paywall-text">Вы прочитали 10 бесплатных книг.<br>Оформите подписку чтобы читать все ' + allBooks.length + ' книг</div>' +
      '<div class="paywall-btn">Оформить подписку</div>' +
      '</div>';
  } else if (!isSubbed) {
    thoughtsHtml += '<div style="text-align:center;padding:12px;color:#888;font-size:12px;">Осталось бесплатных книг: ' + (FREE_BOOKS - freeUsed.length) + '</div>';
  }

  var isRead = readBooks.has(b.id);
  var isFav = favoriteBooks.has(b.id);
  var r = allReactions[String(b.id)] || { up: 0, down: 0 };
  var userVote = localStorage.getItem('vote_' + b.id);
  document.getElementById('detail-content').innerHTML =
    '<div class="detail-hero">' +
    '<div class="detail-cover-wrap">' +
    '<div class="detail-cover">' + coverImg(b.cover, b.title) + '</div>' +
    '<div class="detail-cover-actions"><div class="detail-cover-actions-inner">' +
    '<button class="fav-btn" id="fav-btn" onclick="toggleFavorite(' + b.id + ')">' + (isFav ? '❤️' : '🤍') + '</button>' +
    '<button class="share-btn" onclick="shareBook(' + b.id + ')"><img src="share.png" width="22" height="22" /></button>' +
    '</div></div>' +
    '</div>' +
    '<div class="detail-meta">' +
    '<div class="detail-book-title">' + b.title + '</div>' +
    (b.author && b.author.trim() !== b.title.trim() ? '<div class="detail-book-author">' + b.author + '</div>' : '') +
    (b.genre ? '<div class="detail-book-genre">' + (GENRES.find(function(g){ return g.key === b.genre; }) || {label: b.genre}).label + (b.year ? ' | <span class="detail-year-inline" style="text-transform:none">' + formatYear(b.year) + '</span>' : '') + '</div>' : '') +
    (b.description ? '<div class="detail-book-desc">' + b.description + '</div>' : '') +
    '</div></div>' +
    '<div class="thoughts-title">10 ГЛАВНЫХ МЫСЛЕЙ</div>' +
    '<div class="thoughts-list">' + thoughtsHtml + '</div>' +
    '<div class="detail-actions">' +
    '<button class="react-btn react-btn-up' + (userVote === 'up' ? ' react-btn--active' : '') + '" id="react-up-btn" onclick="doReact(' + b.id + ',\'up\')">' +
    '👍' + (r.up > 0 ? ' <span id="react-up-count">' + r.up + '</span>' : ' <span id="react-up-count" style="display:none">' + r.up + '</span>') +
    '</button>' +
    '<button class="read-btn' + (isRead ? ' read-btn--done' : '') + '" onclick="toggleRead(' + b.id + ')">' +
    (isRead ? '<img src="ok.png" alt="" width="20" height="20" />' : '') +
    '<span>' + (isRead ? 'Прочитал!' : 'Прочитал?') + '</span>' +
    '</button>' +
    '<button class="react-btn react-btn-down' + (userVote === 'down' ? ' react-btn--active' : '') + '" id="react-down-btn" onclick="doReact(' + b.id + ',\'down\')">' +
    (r.down > 0 ? '<span id="react-down-count">' + r.down + '</span> ' : '<span id="react-down-count" style="display:none">' + r.down + '</span> ') +
    '👎</button>' +
    '</div>';

  document.getElementById('detail-content').scrollTop = 0;
  setScreen('detail');
}

function toggleRead(id) {
  if (readBooks.has(id)) {
    readBooks.delete(id);
  } else {
    readBooks.add(id);
  }
  saveReadBooks();
  updateSortLabel();
  var isRead = readBooks.has(id);
  var btn = document.querySelector('.read-btn');
  if (btn) {
    btn.className = 'read-btn' + (isRead ? ' read-btn--done' : '');
    btn.innerHTML = (isRead ? '<img src="ok.png" alt="" width="20" height="20" />' : '') +
      '<span>' + (isRead ? 'Прочитал!' : 'Прочитал?') + '</span>';
  }
}

async function doReact(bookId, type) {
  var prev = localStorage.getItem('vote_' + bookId);
  if (prev) return;
  try {
    var resp = await fetch(API + '/react/' + bookId + '/' + type, { method: 'POST' });
    var data = await resp.json();
    allReactions[String(bookId)] = data;
    localStorage.setItem('vote_' + bookId, type);
    var upEl = document.getElementById('react-up-count');
    var downEl = document.getElementById('react-down-count');
    if (upEl) { upEl.textContent = data.up; upEl.style.display = data.up > 0 ? 'inline' : 'none'; }
    if (downEl) { downEl.textContent = data.down; downEl.style.display = data.down > 0 ? 'inline' : 'none'; }
    var upBtn = document.getElementById('react-up-btn');
    var downBtn = document.getElementById('react-down-btn');
    if (upBtn) upBtn.classList.toggle('react-btn--active', type === 'up');
    if (downBtn) downBtn.classList.toggle('react-btn--active', type === 'down');
  } catch(e) {}
}

function nextBook() {
  var list = currentListForNav.length ? currentListForNav : allBooks;
  var ids = list.map(function(b){ return b.id; });
  var currentId = parseInt(document.getElementById('next-btn').dataset.currentId);
  var idx = ids.indexOf(currentId);
  var nextIdx = (idx + 1) % ids.length;
  openBook(ids[nextIdx]);
}

function prevBook() {
  var list = currentListForNav.length ? currentListForNav : allBooks;
  var ids = list.map(function(b){ return b.id; });
  var currentId = parseInt(document.getElementById('next-btn').dataset.currentId);
  var idx = ids.indexOf(currentId);
  var prevIdx = (idx - 1 + ids.length) % ids.length;
  openBook(ids[prevIdx]);
}

function goHome() {
  document.getElementById('search-bar').style.display = 'none';
  document.getElementById('genre-tabs').style.display = 'flex';
  document.getElementById('search-input').value = '';
  setScreen('list');
  renderList(filterByGenre(allBooks, activeGenre));
  var opt = GENRE_OPTIONS.find(function(o){ return o.key === activeGenre; });
  if (opt) document.getElementById('genre-label').textContent = opt.label;
}

function setScreen(name) {
  ['list','detail','sub'].forEach(function(s) {
    document.getElementById('screen-' + s).classList.remove('active');
  });
  document.getElementById('screen-' + name).classList.add('active');
  document.querySelectorAll('.nav-btn').forEach(function(b){ b.classList.remove('active'); });
  var navMap = { list: '.nav-home', sub: '.nav-sub' };
  if (navMap[name]) document.querySelector(navMap[name]).classList.add('active');
  if (name !== 'list' && name !== 'detail') {
    document.getElementById('scroll-top-btn').classList.remove('visible');
  }
}

var selectedPlan = 'year';

function setSubIcon(premium) {}

function getTgUid() {
  var tg = window.Telegram && window.Telegram.WebApp;
  if (!tg) return null;
  try {
    var uid = tg.initDataUnsafe && tg.initDataUnsafe.user && tg.initDataUnsafe.user.id;
    if (uid) return String(uid);
  } catch(e) {}
  try {
    var params = new URLSearchParams(tg.initData);
    var user = JSON.parse(decodeURIComponent(params.get('user') || '{}'));
    if (user.id) return String(user.id);
  } catch(e) {}
  return null;
}

function applySubscribedUI(expiresStr) {
  setSubIcon(true);
  var badge = document.getElementById('sub-vip-badge');

  var tier = 'start';
  var planName = 'Старт';
  if (expiresStr) {
    var d = new Date(expiresStr);
    var forever = d.getFullYear() > 2100;
    if (forever) {
      tier = 'legend'; planName = 'Легенда';
    } else {
      var days = Math.ceil((d - new Date()) / 86400000);
      if (days > 300) { tier = 'pro'; planName = 'Про'; }
    }
    var infoEl = document.getElementById('sub-info-text');
    if (infoEl) {
      infoEl.textContent = forever
        ? 'Легенда · Навсегда'
        : planName + ' · Осталось ' + days + ' ' + (days === 1 ? 'день' : days < 5 ? 'дня' : 'дней');
    }
  }

  var tierStyles = {
    start:  { bg: 'linear-gradient(90deg,#707088,#a0a0b8)', color: '#fff' },
    pro:    { bg: 'linear-gradient(90deg,#d4a017,#f5d050)', color: '#000' },
    legend: { bg: 'linear-gradient(90deg,#c0204a,#e0306a)', color: '#fff' }
  };
  var s = tierStyles[tier];

  if (badge) {
    badge.innerHTML = '<img src="vip.png" alt="" style="width:16px;height:16px;object-fit:contain;margin-right:5px"> Подписка оформлена';
    badge.style.display = 'flex';
    badge.style.background = s.bg;
    badge.style.color = s.color;
    badge.style.fontSize = '12px';
    badge.style.fontWeight = '700';
    badge.style.borderRadius = '20px';
    badge.style.padding = '5px 12px';
    badge.style.cursor = 'pointer';
    badge.style.alignItems = 'center';
  }
}

async function checkSubscription() {
  var cached = localStorage.getItem('sub_expires');
  if (cached) applySubscribedUI(cached);

  var uid = getTgUid();
  if (!uid) return;
  try {
    var resp = await fetch(API + '/subscription/' + uid);
    var data = await resp.json();
    if (data.subscribed) {
      localStorage.setItem('sub_expires', data.expires || '');
      applySubscribedUI(data.expires);
    } else {
      localStorage.removeItem('sub_expires');
      setSubIcon(false);
      var badge = document.getElementById('sub-vip-badge');
      if (badge) { badge.classList.add('sub-vip-hidden'); badge.classList.remove('sub-vip-active'); }
    }
  } catch(e) {}
}

function showSubInfo() {
  var el = document.getElementById('sub-info-overlay');
  if (el) el.classList.add('show');
}

function closeSubInfo() {
  var el = document.getElementById('sub-info-overlay');
  if (el) el.classList.remove('show');
}

function selectPlan(el, plan) {
  selectedPlan = plan;
  document.querySelectorAll('.sub-plan').forEach(function(b){ b.classList.remove('sub-plan--active'); });
  el.classList.add('sub-plan--active');
}

async function paySelected() {
  var tg = window.Telegram && window.Telegram.WebApp;
  var btn = document.getElementById('sub-pay-btn');
  btn.disabled = true;
  btn.textContent = 'Загрузка...';
  try {
    var resp = await fetch(API + '/invoice/' + selectedPlan);
    var data = await resp.json();
    if (!data.link) throw new Error(data.error || 'no link');
    if (tg && tg.openInvoice) {
      tg.openInvoice(data.link, function(status) {
        if (status === 'paid') {
          setSubIcon(true);
          alert('Спасибо! Подписка активирована.');
        }
      });
    } else if (tg && tg.openLink) {
      tg.openLink(data.link);
    } else {
      window.open(data.link, '_blank');
    }
  } catch(e) {
    alert('Ошибка: ' + e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Оплатить Stars';
  }
}

function openSub() {
  setScreen('sub');
  var cached = localStorage.getItem('sub_expires');
  if (cached) applySubscribedUI(cached);
  checkSubscription();
}

function buyStars() {
  var tg = window.Telegram && window.Telegram.WebApp;
  if (tg && tg.openTelegramLink) {
    tg.openTelegramLink('https://t.me/stars');
  } else {
    window.open('https://t.me/stars', '_blank');
  }
}

function writeAdmin() {
  var tg = window.Telegram && window.Telegram.WebApp;
  if (tg && tg.openTelegramLink) {
    tg.openTelegramLink('https://t.me/rzabeyda');
  } else {
    window.open('https://t.me/rzabeyda', '_blank');
  }
}
function closeSub() { setScreen('list'); renderList(filterByGenre(allBooks, activeGenre)); }

async function buyPlan(plan) {
  var tg = window.Telegram && window.Telegram.WebApp;
  if (!tg || !tg.openInvoice) { alert('Откройте в Telegram'); return; }
  try {
    var resp = await fetch(API + '/invoice/' + plan);
    var data = await resp.json();
    if (!data.link) throw new Error(data.error || 'no link');
    tg.openInvoice(data.link, function(status) {
      if (status === 'paid') alert('Спасибо! Подписка активирована.');
    });
  } catch(e) {
    alert('Ошибка: ' + e.message);
  }
}

function openWhyModal() {
  document.getElementById('why-modal').style.display = 'flex';
}
function closeWhyModal() {
  document.getElementById('why-modal').style.display = 'none';
}

function openDonateModal() {
  document.getElementById('donate-amount-input').value = '';
  document.getElementById('donate-modal').style.display = 'flex';
}
function closeDonateModal() {
  document.getElementById('donate-modal').style.display = 'none';
}
function submitDonate() {
  var amount = parseInt(document.getElementById('donate-amount-input').value);
  if (!amount || amount < 1) { alert('Введи количество звёзд'); return; }
  fetch(API + '/donate?amount=' + amount)
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (!data.link) { alert('Ошибка: ' + (data.error || 'неизвестно')); return; }
      closeDonateModal();
      Telegram.WebApp.openInvoice(data.link, function(status) {
        if (status === 'paid') { alert('Спасибо за поддержку! ⭐'); }
      });
    })
    .catch(function() { alert('Ошибка соединения'); });
}

function closeOnboarding() {
  localStorage.setItem('ob_done', '1');
  document.getElementById('onboarding').style.display = 'none';
}

if (!localStorage.getItem('ob_done')) {
  document.getElementById('onboarding').style.display = 'flex';
}

init();

// Scroll-to-top button
(function() {
  var btn = document.getElementById('scroll-top-btn');
  var threshold = 300;

  function onScroll() {
    if (this.scrollTop > threshold) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }

  function onScrollBooks() {
    var onBooksTab = document.getElementById('screen-list').classList.contains('active') ||
                     document.getElementById('screen-detail').classList.contains('active');
    if (onBooksTab && this.scrollTop > threshold) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }
  document.getElementById('books-list').addEventListener('scroll', onScrollBooks, { passive: true });
  document.getElementById('detail-content').addEventListener('scroll', onScrollBooks, { passive: true });
  document.getElementById('books-list').addEventListener('touchstart', function() { autoScrollStopped = true; }, { passive: true });
  document.getElementById('books-list').addEventListener('click', function() { autoScrollStopped = true; }, { passive: true });
})();

function scrollToTop() {
  var listEl = document.getElementById('books-list');
  var detailEl = document.getElementById('detail-content');
  var target = listEl.scrollTop > 0 ? listEl : detailEl;
  target.scrollTo({ top: 0, behavior: 'smooth' });
}
