import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

# отношения = hex d0bed182d0bdd0bed188d0b5d0bdd0b8d18f (10 chars)
target_hex = "d0bed182d0bdd0bed188d0b5d0bdd0b8d18f"
total_ok = total_short = total_long = 0
for b in books:
    g = b.get("genre", "")
    if g.encode("utf-8").hex() != target_hex:
        continue
    ok = short = long_ = 0
    for i, t in enumerate(b.get("thoughts", [])):
        total = len(t["title"]) + len(t["example"])
        if total < 700:
            short += 1
        elif total <= 900:
            ok += 1
        else:
            long_ += 1
    total_ok += ok
    total_short += short
    total_long += long_
    status = "OK" if short == 0 and long_ == 0 else "PROBLEM"
    print(f"  [{b['id']}] thoughts={ok+short+long_} OK={ok} short={short} long={long_} {status}")

print(f"\nGenre total: OK={total_ok}, short={total_short}, long={total_long}")
