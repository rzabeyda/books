
with open('/root/books/webapp/app.js', 'r') as f:
    js = f.read()

# 1. Remove year from after title
old_year_top = ("'<div class=\"detail-book-title\">' + b.title + '</div>' +\n"
                "    (b.year ? '<div class=\"detail-book-year\">' + b.year + '</div>' : '') +\n"
                "    '<div class=\"detail-book-author\">' + b.author + '</div>' +")
new_year_top = ("'<div class=\"detail-book-title\">' + b.title + '</div>' +\n"
                "    '<div class=\"detail-book-author\">' + b.author + '</div>' +")

if old_year_top in js:
    js = js.replace(old_year_top, new_year_top, 1)
    print('OK: год убран сверху')
else:
    print('ERROR: year-top pattern not found')

# 2. Add year at bottom of meta (after тираж), with formatting
old_reads = ("    (b.world_reads_label ? '<div class=\"detail-reads\">' + b.world_reads_label + '</div>' : '') +")
new_reads = ("    (b.world_reads_label ? '<div class=\"detail-reads\">' + b.world_reads_label + '</div>' : '') +\n"
             "    (b.year ? '<div class=\"detail-book-year\">' + (b.year < 0 ? Math.abs(b.year) + ' г. до н.э.' : b.year + ' г.') + '</div>' : '') +")

if old_reads in js:
    js = js.replace(old_reads, new_reads, 1)
    print('OK: год добавлен внизу с форматированием')
else:
    print('ERROR: reads pattern not found')

with open('/root/books/webapp/app.js', 'w') as f:
    f.write(js)

print('Done.')
