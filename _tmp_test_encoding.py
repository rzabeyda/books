import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)
# test: append Cyrillic to book 598 thought 0 and check
for b in books:
    if b["id"] != 598:
        continue
    t = b["thoughts"][0]
    original = t["example"]
    t["example"] += " Братья Вачовски придумали концепцию пилюли."
    result = t["example"]
    added = result[len(original):]
    has_q = "?" in added
    print(f"Added: {repr(added)}")
    print(f"Has question marks: {has_q}")
    print(f"Length added: {len(added)}")
    # restore
    t["example"] = original
    break
# don't save - just test
