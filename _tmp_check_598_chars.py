import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)
for b in books:
    if b["id"] != 598:
        continue
    bad_count = 0
    for i, t in enumerate(b.get("thoughts", [])):
        ex = t["example"]
        q_count = ex.count("?")
        if q_count > 5:
            bad_count += 1
    print(f"Book 598: thoughts with >5 literal '?': {bad_count}/53")
    # show first bad one
    for i, t in enumerate(b.get("thoughts", [])):
        if t["example"].count("?") > 5:
            ex = t["example"]
            idx = ex.find("?")
            print(f"  [{i}] first ? at pos {idx}, total {len(t['title'])+len(ex)}")
            break
