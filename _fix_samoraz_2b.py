import json

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

for b in books:
    if b["id"] == 113:
        b["description"] = "Тони Роббинс о том как взять под контроль своё мышление, эмоции и действия — и целенаправленно создать ту жизнь которую хочешь."
        print("desc=%d" % len(b["description"]))

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))
