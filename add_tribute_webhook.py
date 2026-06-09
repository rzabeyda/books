content = open('/root/books/server.py').read()

# Add imports at top
old_imports = "import os\nimport json\nimport urllib.request\nimport urllib.parse\nfrom datetime import datetime\nfrom http.server import BaseHTTPRequestHandler, HTTPServer\nfrom urllib.parse import urlparse"

new_imports = "import os\nimport json\nimport hmac\nimport hashlib\nimport urllib.request\nimport urllib.parse\nfrom datetime import datetime, timedelta\nfrom http.server import BaseHTTPRequestHandler, HTTPServer\nfrom urllib.parse import urlparse"

content = content.replace(old_imports, new_imports)

# Add timedelta to existing datetime import (already done above)
# Fix: remove old "from datetime import datetime" since we replaced it
content = content.replace(
    "from datetime import datetime, timedelta\nfrom datetime import datetime\n",
    "from datetime import datetime, timedelta\n"
)

# Add tribute webhook handler in do_POST, before the final else
old_else = '''        else:
            self.send_json(404, {'error': 'not found'})


if __name__ == '__main__':'''

new_tribute = '''        elif path == '/tribute-webhook':
            length = int(self.headers.get('Content-Length', 0))
            body_bytes = self.rfile.read(length)
            # Verify signature
            api_key = os.getenv('TRIBUTE_API_KEY', '')
            if api_key:
                sig = self.headers.get('trbt-signature', '')
                expected = hmac.new(api_key.encode(), body_bytes, hashlib.sha256).hexdigest()
                if not hmac.compare_digest(expected, sig):
                    self.send_json(403, {'error': 'invalid signature'})
                    return
            try:
                event = json.loads(body_bytes)
                name = event.get('name', '')
                payload = event.get('payload', {})
                uid = str(payload.get('telegram_user_id', ''))
                amount = float(payload.get('amount', 0))
                if name in ('new_subscription', 'renewed_subscription') and uid:
                    # Determine period by amount
                    if amount <= 6:
                        days = 30
                        period_label = '1 месяц'
                    elif amount <= 55:
                        days = 365
                        period_label = '1 год'
                    else:
                        days = 36500
                        period_label = 'Навсегда'
                    subs = load_subs()
                    # If renewing, extend from current expiry
                    if uid in subs and days < 36500:
                        current = datetime.fromisoformat(subs[uid])
                        base = max(current, datetime.utcnow())
                    else:
                        base = datetime.utcnow()
                    expires = base + timedelta(days=days)
                    subs[uid] = expires.isoformat()
                    save_subs(subs)
                    # Notify user in Telegram
                    token = os.getenv('BOT_TOKEN')
                    if token and uid:
                        try:
                            exp_str = expires.strftime('%d.%m.%Y') if days < 36500 else 'навсегда'
                            msg = f'✅ Подписка активирована!\\n\\n📚 Доступ открыт на {period_label}\\n📅 Действует до: {exp_str}\\n\\nОткрой библиотеку: /start'
                            data = urllib.parse.urlencode({'chat_id': uid, 'text': msg}).encode()
                            req = urllib.request.Request('https://api.telegram.org/bot' + token + '/sendMessage', data=data)
                            urllib.request.urlopen(req, timeout=10)
                        except Exception:
                            pass
                    # Notify admin
                    try:
                        token = os.getenv('BOT_TOKEN')
                        username = payload.get('telegram_username', '')
                        display = f'@{username}' if username else f'id{uid}'
                        msg_admin = f'💳 Оплата картой/криптой\\n{display} — {period_label} (${amount})'
                        data = urllib.parse.urlencode({'chat_id': '7308147004', 'text': msg_admin}).encode()
                        req = urllib.request.Request('https://api.telegram.org/bot' + token + '/sendMessage', data=data)
                        urllib.request.urlopen(req, timeout=10)
                    except Exception:
                        pass
                self.send_json(200, {'ok': True})
            except Exception as e:
                self.send_json(500, {'error': str(e)})
        else:
            self.send_json(404, {'error': 'not found'})


if __name__ == '__main__':'''

content = content.replace(old_else, new_tribute)

open('/root/books/server.py', 'w').write(content)
print('Done')

# Verify the webhook route was added
if '/tribute-webhook' in open('/root/books/server.py').read():
    print('Webhook route OK')
else:
    print('ERROR: route not added')
