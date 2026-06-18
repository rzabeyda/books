import json, re

def trim_thought(title, example, min_total=700, max_total=800):
    total = len(title) + len(example)
    if total <= max_total:
        return example
    target = max_total - len(title)
    ends = [m.start()+1 for m in re.finditer(r"[.!?](?=\s|»|\n|$)", example)]
    for pos in reversed(ends):
        if pos <= target:
            candidate = example[:pos].rstrip()
            new_total = len(title) + len(candidate)
            if min_total <= new_total <= max_total:
                return candidate
    return example[:target].rstrip()

desc_fixes = {
    458: "Личный дневник императора Рима — стоическая философия как ежедневная практика: как сохранять достоинство, терпение и ясность в любых обстоятельствах.",
    461: "Декарт сомневается во всём — и находит единственную несомненную точку: «Я мыслю, следовательно, существую», заложив фундамент современной философии.",
    462: "Спиноза доказывает геометрически: Бог и природа — одно, свобода воли иллюзорна, а путь к счастью — понимание своих эмоций и законов мироздания.",
    465: "Революционный труд Канта: разум строит реальность, а не просто её отражает — и определяет пределы того что мы можем познать.",
    467: "Путешествие сознания — Гегель показывает что история, культура и мышление развиваются через противоречие и снятие.",
    608: "Афоризмы и философские наблюдения Нассима Талеба — жёсткие и точные мысли о жизни, риске, мышлении и неопределённости.",
}

with open("/root/books/webapp/books.json") as f:
    books = json.load(f)

trimmed = 0
for b in books:
    if b.get("genre") != "философия":
        continue
    bid = b["id"]
    for t in b.get("thoughts", []):
        total = len(t["title"]) + len(t["example"])
        if total > 800:
            t["example"] = trim_thought(t["title"], t["example"])
            trimmed += 1
    if bid in desc_fixes:
        b["description"] = desc_fixes[bid]

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",",":"))
print("Trimmed %s thoughts, %s descriptions" % (trimmed, len(desc_fixes)))
