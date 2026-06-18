import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)
for b in books:
    g = b.get("genre", "")
    if len(g) == 9 and g[0] == "о" and g[1] == "т":
        ok = short = long_ = 0
        for t in b.get("thoughts", []):
            total = len(t["title"]) + len(t["example"])
            if total < 700: short += 1
            elif total <= 900: ok += 1
            else: long_ += 1
        status = "OK" if short == 0 and long_ == 0 else "PROBLEM"
        print(f"  [{b['id']}] {b.get('title','')[:35]}: OK={ok} short={short} long={long_} {status}")
