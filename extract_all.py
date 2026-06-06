import json, sys, os

SESSIONS = [
    r"C:\Users\rzabe\.claude\projects\C--books\8ffd638b-22f9-4607-ba6f-d14eeb1d1e81.jsonl",
    r"C:\Users\rzabe\.claude\projects\C--books\453b8568-314c-4ceb-af25-6a315d4a3f02.jsonl",
    r"C:\Users\rzabe\.claude\projects\C--books\95871b26-132b-4b6e-acf1-20481b6ee757.jsonl",
]

KEYWORDS = ['7 навыков', 'Богатый папа', 'Дневник Анны', 'Исцели', 'Ребёнок и уход',
            'Спок', 'Луиза Хей', 'Кови', 'Карнеги', 'Мужчины с Марса', 'Секрет',
            'Долгий путь', 'Великая шахматная', 'Неудобная правда', 'Доминанта',
            'Схема-терапия', 'Наука быть живым', 'Психология в кино', '1984', 'Оруэлл',
            'Позитивного мышления']

scripts_found = []

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
                                script_content = inp.get('content', '')
                                if 'thoughts' in script_content:
                                    has_keyword = any(k in script_content for k in KEYWORDS)
                                    if has_keyword:
                                        key = sess_name + '_' + inp['file_path'].split('\\')[-1].split('/')[-1]
                                        scripts_found.append((key, script_content))
                                        sys.stdout.buffer.write(f"Found: {key} ({len(script_content)} chars)\n".encode())
        except:
            pass

sys.stdout.buffer.write(f"\nTotal: {len(scripts_found)} scripts\n".encode())

seen = set()
for i, (name, content) in enumerate(scripts_found):
    if content in seen:
        continue
    seen.add(content)
    out = rf"C:\books\rec2_script_{i}.py"
    with open(out, 'w', encoding='utf-8') as f:
        f.write(content)
    sys.stdout.buffer.write(f"Saved: {out}\n".encode())
