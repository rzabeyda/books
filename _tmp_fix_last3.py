import json
with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

appends = {
334: {
    7: " Клон — это запаздывающий близнец в другом времени и с другой историей. Два человека с идентичным ДНК были бы разными людьми.",
    8: " Синтетическая биология ставит вопрос об авторстве жизни: если мы пишем геном — кто несёт ответственность за организм. Право не успевает за наукой.",
},
335: {
    2: " Если дополнительные измерения существуют на субъядерном уровне — мы никогда не почувствуем их напрямую. Только через последствия: гравитацию утекающую в невидимые измерения.",
},
}

count = 0
for b in books:
    if b["id"] not in appends:
        continue
    for i, t in enumerate(b.get("thoughts", [])):
        if i in appends[b["id"]]:
            t["example"] += appends[b["id"]][i]
            s = len(t["title"]) + len(t["example"])
            print(f"[{b['id']}][{i}] -> {s}")
            count += 1

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",",":"))
print(f"Fixed: {count}")
