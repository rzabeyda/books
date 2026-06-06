import json, re, sys

SESSION = r"C:\Users\rzabe\.claude\projects\C--books\95871b26-132b-4b6e-acf1-20481b6ee757.jsonl"

with open(SESSION, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find all Python script content written to files (Write tool calls)
scripts = []
for line in lines:
    try:
        obj = json.loads(line)
        # look for assistant messages with tool use
        msg = obj.get('message', {})
        if isinstance(msg, dict):
            content = msg.get('content', [])
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get('type') == 'tool_use':
                        tool = block.get('name', '')
                        inp = block.get('input', {})
                        # Write tool - look for Python files with thoughts
                        if tool == 'Write' and inp.get('file_path', '').endswith('.py'):
                            script_content = inp.get('content', '')
                            if 'thoughts' in script_content and ('bhagavad' in script_content.lower() or 'tripitaka' in script_content.lower() or 'искусство' in script_content.lower() or 'мао' in script_content.lower() or 'библия' in script_content.lower() or 'коран' in script_content.lower()):
                                scripts.append((inp['file_path'], script_content))
                                sys.stdout.buffer.write(f"Found script: {inp['file_path']} ({len(script_content)} chars)\n".encode())
    except:
        pass

sys.stdout.buffer.write(f"\nTotal scripts found: {len(scripts)}\n".encode())

# Save all scripts
for i, (path, content) in enumerate(scripts):
    out_path = rf"C:\books\recovered_script_{i}.py"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    sys.stdout.buffer.write(f"Saved: {out_path}\n".encode())
