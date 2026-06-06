import json, sys, os

SESSIONS = [
    r"C:\Users\rzabe\.claude\projects\C--books\070b8f75-649b-4255-8f3e-8958bfd79367.jsonl",
    r"C:\Users\rzabe\.claude\projects\C--books\8ffd638b-22f9-4607-ba6f-d14eeb1d1e81.jsonl",
    r"C:\Users\rzabe\.claude\projects\C--books\453b8568-314c-4ceb-af25-6a315d4a3f02.jsonl",
    r"C:\Users\rzabe\.claude\projects\C--books\95871b26-132b-4b6e-acf1-20481b6ee757.jsonl",
]

KEYWORDS = ['Доминанта', 'Великая шахматная', 'Схема-терапия', 'Наука быть живым',
            'Психология в кино', 'Неудобная правда', 'Как избавиться от переутомления',
            'Сила позитивного', 'Долгий путь к свободе', 'Мандела']

scripts_found = []
seen_content = set()

for SESSION in SESSIONS:
    sess_name = os.path.basename(SESSION)[:8]
    with open(SESSION, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        try:
            obj = json.loads(line)
            msg = obj.get('message', {})
            if isinstance(msg, dict):
                content = msg.get('content', [])
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get('type') == 'tool_use':
                            tool = block.get('name', '')
                            inp = block.get('input', {})
                            if tool == 'Write' and str(inp.get('file_path', '')).endswith('.py'):
                                sc = inp.get('content', '')
                                if 'thoughts' in sc and any(k in sc for k in KEYWORDS):
                                    sig = sc[:200]
                                    if sig not in seen_content:
                                        seen_content.add(sig)
                                        fname = inp['file_path'].split('\\')[-1].split('/')[-1]
                                        key = f"{sess_name}_{fname}"
                                        scripts_found.append((key, sc))
                                        sys.stdout.buffer.write(f"Found: {key} ({len(sc)} chars)\n".encode())
        except:
            pass

sys.stdout.buffer.write(f"\nTotal unique: {len(scripts_found)}\n".encode())

for i, (name, content) in enumerate(scripts_found):
    out = rf"C:\books\rec3_script_{i}.py"
    with open(out, 'w', encoding='utf-8') as f:
        f.write(content)
    sys.stdout.buffer.write(f"Saved: {out}\n".encode())
