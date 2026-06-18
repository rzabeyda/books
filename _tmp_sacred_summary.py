import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

for b in books:
    if b.get("genre") != "священные писания":
        continue
    desc = b.get("description", "")
    print(f"[{b['id']}] desc={len(desc)} | {b.get('title','')}")
    for i, t in enumerate(b.get("thoughts", [])):
        total = len(t["title"]) + len(t["example"])
        flag = "SHORT" if total < 700 else ("LONG" if total > 900 else "ok")
        print(f"  [{i}] {total} {flag} | {t['title'][:50]}")
