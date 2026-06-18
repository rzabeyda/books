import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

# Read short thoughts from books 362,363,364,365,531 + specific short ones from 40,42,52,53,87,248
short_map = {
    40: [4], 42: [0,2,8], 52: [0,1,2,3,4,5,6], 53: [2],
    87: [1,2,4,5,6,8,9],
    248: list(range(10)),
    362: list(range(10)), 363: list(range(10)),
    364: list(range(10)), 365: list(range(10)),
    531: [1,2,3,4,5,6,7,8,9],
}
for b in books:
    bid = b["id"]
    if bid not in short_map:
        continue
    print(f"\n=== [{bid}] {b.get('title','')} ===")
    for i, t in enumerate(b.get("thoughts", [])):
        if i not in short_map[bid]:
            continue
        total = len(t["title"]) + len(t["example"])
        print(f"[{i}] ({total}) {t['title']}")
        print(f"  {t['example']}")
