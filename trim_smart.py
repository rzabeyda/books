import json

with open("/root/books/webapp/books.json", "r", encoding="utf-8") as f:
    books = json.load(f)

TARGET = 950
MIN_LIFE = 40
count = 0

for b in books:
    for t in b.get("thoughts", []):
        total = len(t["title"]) + len(t["example"])
        if total <= 1000:
            continue
        ex = t["example"]
        life_marker = "\n\n**В жизни:**"
        life_start = ex.find(life_marker)
        if life_start < 0:
            continue

        base = ex[:life_start]
        life_text = ex[life_start + len(life_marker):].lstrip(" ")

        # how much total space for base + life?
        budget = TARGET - len(t["title"]) - len(life_marker) - 1  # -1 for space after marker

        # keep at least MIN_LIFE for life text
        max_base = budget - MIN_LIFE

        if len(base) > max_base:
            # trim base text at sentence boundary
            trimmed_base = base[:max_base]
            for punct in [". ", "! ", "? "]:
                last = trimmed_base.rfind(punct)
                if last > max_base // 2:
                    trimmed_base = trimmed_base[:last + 1]
                    break
            else:
                last_space = trimmed_base.rfind(" ")
                if last_space > max_base // 2:
                    trimmed_base = trimmed_base[:last_space]
            base = trimmed_base.rstrip()

        # now trim life text if still over
        remaining = TARGET - len(t["title"]) - len(base) - len(life_marker) - 1
        if remaining < MIN_LIFE:
            remaining = MIN_LIFE
        if len(life_text) > remaining:
            trimmed_life = life_text[:remaining]
            for punct in [". ", "! ", "? "]:
                last = trimmed_life.rfind(punct)
                if last > remaining // 2:
                    trimmed_life = trimmed_life[:last + 1]
                    break
            else:
                last_space = trimmed_life.rfind(" ")
                if last_space > remaining // 2:
                    trimmed_life = trimmed_life[:last_space]
            life_text = trimmed_life.rstrip()

        t["example"] = base + life_marker + " " + life_text
        count += 1

with open("/root/books/webapp/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, separators=(",", ":"))
print(f"Trimmed {count} thoughts")
