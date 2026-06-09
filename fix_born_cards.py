content = open('/root/books/webapp/app.js').read()

# Add born to top card
old1 = """'<div class="top-card-author">' + b.author + '</div>' +
    (b.world_reads_label ? '<div class="top-card-reads">' + b.world_reads_label + '</div>' : '') +"""
new1 = """'<div class="top-card-author">' + b.author + '</div>' +
    (b.born ? '<div class="top-card-born">' + b.born + '</div>' : '') +
    (b.world_reads_label ? '<div class="top-card-reads">' + b.world_reads_label + '</div>' : '') +"""
content = content.replace(old1, new1)

# Add born to book card
old2 = """'<div class="book-author">' + b.author + '</div>' +
      (b.world_reads_label ? '<div class="book-reads">' + b.world_reads_label + '</div>' : '') +"""
new2 = """'<div class="book-author">' + b.author + '</div>' +
      (b.born ? '<div class="book-born">' + b.born + '</div>' : '') +
      (b.world_reads_label ? '<div class="book-reads">' + b.world_reads_label + '</div>' : '') +"""
content = content.replace(old2, new2)

open('/root/books/webapp/app.js', 'w').write(content)
print('top-card-born' in content, 'book-born' in content)
