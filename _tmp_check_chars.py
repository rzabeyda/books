import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)
for b in books:
    if b["id"] != 632:
        continue
    t = b["thoughts"][0]
    ex = t["example"]
    # find suspicious area - last 100 chars
    tail = ex[-100:]
    print(f"Last 100 chars of thought 0:")
    for i, c in enumerate(tail):
        if ord(c) == 63:  # literal ?
            print(f"  LITERAL ? at pos {len(ex)-100+i}")
        elif ord(c) < 32 or (128 <= ord(c) <= 159):
            print(f"  BAD char {ord(c)} at pos {len(ex)-100+i}")
    # print last 200 chars as unicode escapes
    print(f"Last 80 chars (unicode): {tail[-80:].encode('unicode_escape').decode()}")
