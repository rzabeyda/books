import json

with open("/root/books/webapp/books.json", "r", encoding="utf-8") as f:
    books = json.load(f)

TARGET = 920
count = 0

for b in books:
    for t in b.get("thoughts", []):
        total = len(t["title"]) + len(t["example"])
        if total <= 1000:
            continue
        ex = t["example"]
        life_start = ex.find("\n\n**В жизни:**")
        if life_start < 0:
            continue
        base = ex[:life_start]
        life_text = ex[life_start + 14:]  # after "\n\n**В жизни:** "
        # how much life text can we keep?
        keep = TARGET - len(t["title"]) - len(base) - 14
        if keep < 50:
            keep = 50
        trimmed = life_text[:keep]
        # try to end at sentence boundary
        for punct in [". ", "! ", "? ", ".\n", "…"]:
            last = trimmed.rfind(punct)
            if last > keep // 2:
                trimmed = trimmed[:last + 1]
                break
        else:
            # end at last space
            last_space = trimmed.rfind(" ")
            if last_space > keep // 2:
                trimmed = trimmed[:last_space]
        t["example"] = base + "\n\n**В жизни:** " + trimmed.rstrip()
        count += 1

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))
print(f"Trimmed {count} thoughts")
