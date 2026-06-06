import json, sys

SESSIONS = [
    r"C:\Users\rzabe\.claude\projects\C--books\95871b26-132b-4b6e-acf1-20481b6ee757.jsonl",
    r"C:\Users\rzabe\.claude\projects\C--books\453b8568-314c-4ceb-af25-6a315d4a3f02.jsonl",
    r"C:\Users\rzabe\.claude\projects\C--books\8ffd638b-22f9-4607-ba6f-d14eeb1d1e81.jsonl",
    r"C:\Users\rzabe\.claude\projects\C--books\070b8f75-649b-4255-8f3e-8958bfd79367.jsonl",
]

def extract_text(obj):
    texts = []
    if isinstance(obj, str):
        texts.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            texts.extend(extract_text(v))
    elif isinstance(obj, list):
        for item in obj:
            texts.extend(extract_text(item))
    return texts

def try_extract_books(text):
    for marker in ['[{"id":1,', '[{"id": 1,']:
        idx = text.find(marker)
        if idx != -1:
            fragment = text[idx:]
            depth = 0
            end = 0
            for i, ch in enumerate(fragment):
                if ch == '[': depth += 1
                elif ch == ']':
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
            try:
                data = json.loads(fragment[:end])
                return data
            except:
                pass
    return None

best_data = None
best_count = 0

for SESSION in SESSIONS:
    with open(SESSION, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        try:
            obj = json.loads(line)
            all_texts = extract_text(obj)
            for text in all_texts:
                if '"world_reads"' in text:
                    data = try_extract_books(text)
                    if data and len(data) > best_count:
                        best_count = len(data)
                        best_data = data
                        short_name = SESSION.split('\\')[-1][:8]
                        sys.stdout.buffer.write(f"New best: {len(data)} books in {short_name}\n".encode())
        except:
            pass

if best_data:
    sys.stdout.buffer.write(f"TOTAL BEST: {len(best_data)} books\n".encode())
    for b in best_data:
        n = len(b.get('thoughts', []))
        has_full = any('В жизни' in t.get('example','') for t in b.get('thoughts',[]))
        flag = b'FULL' if has_full else (b'EMPTY' if n==0 else b'SHORT')
        line_out = f"  id={b['id']} [{n}] ".encode() + flag + f" - {b['title']}\n".encode('utf-8')
        sys.stdout.buffer.write(line_out)
    with open(r"C:\books\books_recovered.json", 'w', encoding='utf-8') as f:
        json.dump(best_data, f, ensure_ascii=False, separators=(',',':'))
    sys.stdout.buffer.write(b"Saved to books_recovered.json\n")
else:
    sys.stdout.buffer.write(b"Nothing found\n")
