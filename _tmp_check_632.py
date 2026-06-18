import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)
for b in books:
    if b["id"] != 632:
        continue
    for i, t in enumerate(b.get("thoughts", [])):
        total = len(t["title"]) + len(t["example"])
        ex = t["example"]
        # check for replacement chars
        has_bad = "�" in ex or "?" * 3 in ex
        print(f"[{i}] {total} bad={has_bad}")
        if has_bad:
            # find where garbage starts
            idx = ex.find("?")
            print(f"  ...{repr(ex[max(0,idx-50):idx+20])}")
