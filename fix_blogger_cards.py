content = open('/root/books/webapp/app.js').read()

old = """      '<div class="book-title">' + b.title + '</div>' +
      '<div class="book-author">' + b.author + '</div>' +
      (b.born ? '<div class="book-born">' + b.born + '</div>' : '') +
      (b.world_reads_label ? '<div class="book-reads">' + b.world_reads_label + '</div>' : '') +"""

new = """      '<div class="book-title">' + b.title + '</div>' +
      (b.platform ? '<div class="book-author">' + b.platform + ' Блогер</div>' : '<div class="book-author">' + b.author + '</div>') +
      (b.subs_label ? '<div class="book-reads">' + b.subs_label + '</div>' : (b.born ? '<div class="book-born">' + b.born + '</div>' : '')) +
      (!b.subs_label && b.world_reads_label ? '<div class="book-reads">' + b.world_reads_label + '</div>' : '') +"""

content = content.replace(old, new)
open('/root/books/webapp/app.js', 'w').write(content)
print('done')
