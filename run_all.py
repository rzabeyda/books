import json, sys, os, re

LOCAL = r"C:\books\books.json"

# Load current books
with open(LOCAL, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Start: {len(data)} books")

# Run each recovered script by patching the path
scripts = [
    r"C:\books\recovered_script_0.py",
    r"C:\books\recovered_script_1.py",
    r"C:\books\recovered_script_2.py",
    r"C:\books\recovered_script_3.py",
    r"C:\books\recovered_script_4.py",
    r"C:\books\recovered_script_5.py",
    r"C:\books\recovered_script_6.py",
    r"C:\books\recovered_script_7.py",
    r"C:\books\recovered_script_8.py",
]

for script_path in scripts:
    with open(script_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Patch all server paths to local path
    code = code.replace('/root/books/webapp/books.json', LOCAL.replace('\\', '\\\\'))
    code = code.replace('/root/books/books.json', LOCAL.replace('\\', '\\\\'))

    # Execute
    try:
        exec(code, {'__file__': script_path})
        # Reload data after each script modifies the file
        with open(LOCAL, 'r', encoding='utf-8') as f:
            data = json.load(f)

        full_count = sum(1 for b in data if b.get('thoughts') and any('В жизни' in t.get('example','') for t in b['thoughts']))
        short_count = sum(1 for b in data if b.get('thoughts') and not any('В жизни' in t.get('example','') for t in b['thoughts']))
        empty_count = sum(1 for b in data if not b.get('thoughts'))
        print(f"  After {os.path.basename(script_path)}: FULL={full_count} SHORT={short_count} EMPTY={empty_count}")
    except Exception as e:
        print(f"  ERROR in {os.path.basename(script_path)}: {e}")

# Final status
print("\nFinal status:")
for b in data:
    n = len(b.get('thoughts', []))
    has_full = any('В жизни' in t.get('example','') for t in b.get('thoughts',[])) if n > 0 else False
    flag = 'FULL' if has_full else ('EMPTY' if n==0 else 'SHORT')
    if flag != 'EMPTY':
        sys.stdout.buffer.write(f"  id={b['id']} [{n}] {flag} - {b['title']}\n".encode('utf-8'))
