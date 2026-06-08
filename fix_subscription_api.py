import subprocess

# 1. Add /subscription/<uid> endpoint to counter.py
with open('/root/books/counter.py', encoding='utf-8') as f:
    code = f.read()

sub_route = """
SUBS_FILE = '/root/books/subscriptions.json'

@app.route('/subscription/<uid>')
def get_subscription(uid):
    from datetime import datetime
    subs = {}
    if os.path.exists(SUBS_FILE):
        subs = json.load(open(SUBS_FILE))
    if uid not in subs:
        return jsonify({'subscribed': False})
    expires_str = subs[uid]
    expires = datetime.fromisoformat(expires_str)
    active = expires > datetime.utcnow()
    return jsonify({'subscribed': active, 'expires': expires_str})
"""

# Insert before the __main__ block
code = code.replace("if __name__ == '__main__':", sub_route + "\nif __name__ == '__main__':")

with open('/root/books/counter.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('counter.py updated')

# 2. Add /subscription/ location to nginx config
with open('/etc/nginx/sites-enabled/books.zabeyda.lol', encoding='utf-8') as f:
    nginx = f.read()

old_reads = """    location /reads {
        proxy_pass http://127.0.0.1:8081/reads;
    }"""
new_reads = """    location /subscription/ {
        proxy_pass http://127.0.0.1:8081;
    }

    location /reads {
        proxy_pass http://127.0.0.1:8081/reads;
    }"""

nginx = nginx.replace(old_reads, new_reads, 1)

with open('/etc/nginx/sites-enabled/books.zabeyda.lol', 'w', encoding='utf-8') as f:
    f.write(nginx)

print('nginx config updated')

# 3. Test nginx config
import subprocess
r = subprocess.run(['nginx', '-t'], capture_output=True, text=True)
print(r.stdout, r.stderr)
if r.returncode == 0:
    subprocess.run(['systemctl', 'reload', 'nginx'])
    print('nginx reloaded')
else:
    print('nginx config ERROR — not reloaded')

# 4. Restart counter.py service
r2 = subprocess.run(['systemctl', 'restart', 'books-counter'], capture_output=True, text=True)
print('counter restart:', r2.returncode, r2.stderr)
