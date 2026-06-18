import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)
for b in books:
    if b["id"] != 598:
        continue
    short = ok = long_ = 0
    for i, t in enumerate(b.get("thoughts", [])):
        total = len(t["title"]) + len(t["example"])
        q_in_ext = t["example"].count("?")
        if total < 700:
            short += 1
            print(f"  SHORT [{i}] {total} q={q_in_ext}: {t['title'][:40]}")
        elif total <= 900:
            ok += 1
        else:
            long_ += 1
            print(f"  LONG [{i}] {total}: {t['title'][:40]}")
    print(f"Book 598: OK={ok} short={short} long={long_}")
