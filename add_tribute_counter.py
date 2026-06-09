content = open('/root/books/counter.py').read()

old = "if __name__ == '__main__':\n    app.run(host='127.0.0.1', port=8081)"

new = '''@app.route('/suggest', methods=['POST', 'OPTIONS'])
def suggest():
    if request.method == 'OPTIONS':
        return '', 200
    text = (request.json or {}).get('text', '').strip()
    if not text:
        return jsonify({'error': 'empty'}), 400
    try:
        token = open('/root/books/.env').read().split('BOT_TOKEN=')[1].split()[0]
        data = urllib.parse.urlencode({'chat_id': '7308147004', 'text': '📚 Предложение книги:\\n' + text}).encode()
        req = urllib.request.Request('https://api.telegram.org/bot' + token + '/sendMessage', data=data)
        urllib.request.urlopen(req, timeout=10)
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/tribute-webhook', methods=['POST'])
def tribute_webhook():
    import hmac as hmac_mod, hashlib
    from datetime import datetime, timedelta
    body = request.get_data()
    api_key = ''
    try:
        env = open('/root/books/.env').read()
        for line in env.splitlines():
            if line.startswith('TRIBUTE_API_KEY='):
                api_key = line.split('=', 1)[1].strip()
    except Exception:
        pass
    if api_key:
        sig = request.headers.get('trbt-signature', '')
        expected = hmac_mod.new(api_key.encode(), body, hashlib.sha256).hexdigest()
        if not hmac_mod.compare_digest(expected, sig):
            return jsonify({'error': 'invalid signature'}), 403
    try:
        event = request.json or {}
        name = event.get('name', '')
        payload = event.get('payload', {})
        uid = str(payload.get('telegram_user_id', ''))
        amount = float(payload.get('amount', 0))
        if name in ('new_subscription', 'renewed_subscription') and uid:
            if amount <= 6:
                days = 30
                period_label = '1 месяц'
            elif amount <= 55:
                days = 365
                period_label = '1 год'
            else:
                days = 36500
                period_label = 'Навсегда'
            subs = {}
            if os.path.exists(SUBS_FILE):
                subs = json.load(open(SUBS_FILE))
            if uid in subs and days < 36500:
                current = datetime.fromisoformat(subs[uid])
                base = max(current, datetime.utcnow())
            else:
                base = datetime.utcnow()
            expires = base + timedelta(days=days)
            subs[uid] = expires.isoformat()
            json.dump(subs, open(SUBS_FILE, 'w'))
            token = open('/root/books/.env').read().split('BOT_TOKEN=')[1].split()[0]
            exp_str = expires.strftime('%d.%m.%Y') if days < 36500 else 'навсегда'
            # Notify user
            try:
                msg = f'✅ Подписка активирована!\\n\\n📚 Доступ открыт на {period_label}\\n📅 Действует до: {exp_str}\\n\\nОткрой библиотеку: /start'
                data = urllib.parse.urlencode({'chat_id': uid, 'text': msg}).encode()
                req = urllib.request.Request('https://api.telegram.org/bot' + token + '/sendMessage', data=data)
                urllib.request.urlopen(req, timeout=10)
            except Exception:
                pass
            # Notify admin
            try:
                username = payload.get('telegram_username', '')
                display = f'@{username}' if username else f'id{uid}'
                msg_admin = f'💳 Оплата картой/криптой\\n{display} — {period_label} (${amount})'
                data = urllib.parse.urlencode({'chat_id': '7308147004', 'text': msg_admin}).encode()
                req = urllib.request.Request('https://api.telegram.org/bot' + token + '/sendMessage', data=data)
                urllib.request.urlopen(req, timeout=10)
            except Exception:
                pass
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081)'''

if "if __name__ == '__main__':" in content:
    content = content.replace(old, new)
    open('/root/books/counter.py', 'w').write(content)
    print('Done')
else:
    print('NOT FOUND')
