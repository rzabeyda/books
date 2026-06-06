var allBooks = [];
var API = 'https://books.zabeyda.lol';
var readBooks = new Set(JSON.parse(localStorage.getItem('readBooks') || '[]'));
var activeGenre = 'all';
var activeSort = 'sales';
var currentListForNav = [];

var SORT_OPTIONS = [
  { key: 'sales',       label: 'По продажам' },
  { key: 'recommended', label: 'Рекомендованные' },
  { key: 'az',          label: 'По названию А → Я' },
  { key: 'za',          label: 'По названию Я → А' },
  { key: 'author',      label: 'По автору А → Я' },
  { key: 'authorza',    label: 'По автору Я → А' },
  { key: 'read',        label: 'Прочитанные' },
  { key: 'unread',      label: 'Не прочитанные' },
];

var GENRE_OPTIONS = [
  { key: 'all',       label: 'Все книги' },
  { key: 'nonfiction',label: 'Нон-фикшн' },
  { key: 'religion',  label: 'Священные писания' },
  { key: 'politics',  label: 'Политика' },
  { key: 'fiction',   label: 'Классика' },
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
  if (sort === 'sales')    return s.sort(function(a,b){ return b.world_reads - a.world_reads; });
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
    list.innerHTML = GENRE_OPTIONS.map(function(o) {
      var active = o.key === activeGenre;
      var count = o.key === 'all' ? allBooks.length : allBooks.filter(function(b){ return b.genre === o.key; }).length;
      return '<button class="sheet-item' + (active ? ' active' : '') + '" onclick="applyGenre(\'' + o.key + '\')">' +
        o.label + '<span class="sheet-count">' + count + '</span>' + (active ? '<span class="sheet-check">✓</span>' : '') + '</button>';
    }).join('');
  }

  overlay.classList.add('show');
  sheet.classList.add('show');
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

function applyGenre(key) {
  activeGenre = key;
  var opt = GENRE_OPTIONS.find(function(o){ return o.key === key; });
  document.getElementById('genre-label').textContent = opt.label;
  closeSheet();
  renderList(filterByGenre(allBooks, activeGenre));
}

function openSearch() {
  document.getElementById('screen-detail').classList.remove('active');
  document.getElementById('screen-list').classList.add('active');
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
  try {
    var booksRes = await fetch(API + '/books.json');
    allBooks = await booksRes.json();
    renderList(allBooks);
  } catch(e) {
    document.getElementById('books-list').innerHTML = '<div class="empty-state">Ошибка загрузки</div>';
  }

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
  return '<img src="' + src + '" alt="' + alt + '" loading="lazy" onerror="this.style.display=\'none\'">';
}

function filterByGenre(books, genre) {
  if (genre === 'all') return books;
  return books.filter(function(b) { return b.genre === genre; });
}

var GENRES = [
  { key: 'nonfiction', label: 'Нон-фикшн' },
  { key: 'religion',   label: 'Священные писания' },
  { key: 'fiction',    label: 'Классика' },
];

function topCardHtml(b) {
  var isRead = readBooks.has(b.id);
  return '<div class="top-card' + (isRead ? ' read' : '') + '" onclick="openBook(' + b.id + ')">' +
    '<div class="top-img">' + coverImg(b.cover, b.title) + '</div>' +
    '<div class="top-card-title">' + b.title + '</div>' +
    '<div class="top-card-author">' + b.author + '</div>' +
    (b.world_reads_label ? '<div class="top-card-reads">' + b.world_reads_label + '</div>' : '') +
    '</div>';
}

function renderList(books) {
  var sorted = sortBooks(books, activeSort);
  currentListForNav = sorted;

  var genreHtml = '';
  var searching = books.length !== allBooks.length;

  if (!searching) {
    GENRES.forEach(function(g) {
      var inGenre = sorted.filter(function(b) { return b.genre === g.key; });
      if (!inGenre.length) return;
      genreHtml +=
        '<div class="section-label">' + g.label + '</div>' +
        '<div class="top-scroll">' + inGenre.slice(0, 8).map(topCardHtml).join('') + '</div>';
    });
  }

  var gridHtml = sorted.map(function(b) {
    var isRead = readBooks.has(b.id);
    return '<div class="book-card' + (isRead ? ' read' : '') + '" onclick="openBook(' + b.id + ')">' +
      '<div class="grid-img">' + coverImg(b.cover, b.title) + '</div>' +
      '<div class="book-info">' +
      '<div class="book-title">' + b.title + '</div>' +
      '<div class="book-author">' + b.author + '</div>' +
      (b.world_reads_label ? '<div class="book-reads">' + b.world_reads_label + '</div>' : '') +
      '</div></div>';
  }).join('');

  document.getElementById('books-list').innerHTML =
    '<div class="books-grid">' + (gridHtml || '<div class="empty-state">Ничего не найдено</div>') + '</div>';
}

function openBook(id) {
  var b = allBooks.filter(function(x) { return x.id === id; })[0];
  if (!b) return;

  document.getElementById('detail-title-top').textContent = b.title;
  document.getElementById('next-btn').dataset.currentId = b.id;

  var thoughtsHtml = b.thoughts.map(function(t, i) {
    return '<div class="thought-card">' +
      '<div class="thought-num">№' + (i + 1) + '</div>' +
      '<div class="thought-title">' + t.title + '</div>' +
      '<div class="thought-example">' + md(t.example) + '</div>' +
      '</div>';
  }).join('');

  var isRead = readBooks.has(b.id);
  document.getElementById('detail-content').innerHTML =
    '<div class="detail-hero">' +
    '<div class="detail-cover">' + coverImg(b.cover, b.title) + '</div>' +
    '<div class="detail-meta">' +
    '<div class="detail-book-title">' + b.title + '</div>' +
    '<div class="detail-book-author">' + b.author + '</div>' +
    '<div class="detail-badge">' + b.thoughts.length + ' главных мыслей</div>' +
    '</div></div>' +
    '<div class="thoughts-title">Ключевые идеи</div>' +
    '<div class="thoughts-list">' + thoughtsHtml + '</div>' +
    '<button class="read-btn' + (isRead ? ' read-btn--done' : '') + '" onclick="toggleRead(' + b.id + ')">' +
    (isRead ? '<img src="ok.png" alt="" width="20" height="20" />' : '') +
    '<span>' + (isRead ? 'Прочитал!' : 'Прочитал?') + '</span>' +
    '</button>';

  document.getElementById('screen-list').classList.remove('active');
  document.getElementById('screen-detail').classList.add('active');
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
  document.getElementById('screen-detail').classList.remove('active');
  document.getElementById('screen-list').classList.add('active');
  renderList(filterByGenre(allBooks, activeGenre));
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

  document.getElementById('books-list').addEventListener('scroll', onScroll, { passive: true });
  document.getElementById('detail-content').addEventListener('scroll', onScroll, { passive: true });
})();

function scrollToTop() {
  var listEl = document.getElementById('books-list');
  var detailEl = document.getElementById('detail-content');
  var target = listEl.scrollTop > 0 ? listEl : detailEl;
  target.scrollTo({ top: 0, behavior: 'smooth' });
}
