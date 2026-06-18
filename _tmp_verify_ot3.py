import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

done_ids = {470, 587, 588, 597, 598, 627}
total_ok = total_short = total_long = 0
for b in books:
    if b.get("genre") != "от автора":
        continue
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
    marker = "" if b["id"] in done_ids else " <-- new"
    print(f"  [{b['id']}] OK={ok} short={short} long={long_} {status}{marker}")

print(f"\nGenre total: OK={total_ok}, short={total_short}, long={total_long}")
