import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

genre_books = [b for b in books if b.get("genre") == "от автора"]
print(f"Books in genre: {len(genre_books)}")

total_ok = total_short = total_long = 0
for b in genre_books:
    ok = short = long_ = 0
    for t in b.get("thoughts", []):
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
    print(f"  [{b['id']}] {b.get('title','?')[:40]}: OK={ok}, short={short}, long={long_} {status}")

print(f"\nTotal: OK={total_ok}, short={total_short}, long={total_long}")
