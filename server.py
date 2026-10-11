import os
import json
import sqlite3
import hmac
import hashlib
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
import time
import sys
from urllib.parse import urlparse

# load .env
_env = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(_env):
    for _line in open(_env):
        _line = _line.strip()
        if _line and '=' in _line and not _line.startswith('#'):
            _k, _v = _line.split('=', 1)
            os.environ.setdefault(_k.strip(), _v.strip())

DB_FILE = '/root/books/books.db'

READS_FILE = '/root/books/reads.json'
SUBS_FILE = '/root/books/subscriptions.json'
REACTIONS_FILE = '/root/books/reactions.json'


def load_subs():
    try:
        with open(SUBS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def is_subscribed_db(user_id: str) -> bool:
    try:
        conn = sqlite3.connect(DB_FILE)
        row = conn.execute(
            "SELECT expires FROM subscriptions WHERE key=?", (user_id,)
        ).fetchone()
        conn.close()
        if not row:
            return False
        return datetime.fromisoformat(row[0]) > datetime.utcnow()
    except Exception:
        return False


def save_subscription_db(user_id: str, expires: datetime):
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute(
            "INSERT OR REPLACE INTO subscriptions (key, expires) VALUES (?,?)",
            (user_id, expires.isoformat())
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def load_reads():
    try:
        with open(READS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


DATA_LOCK = threading.Lock()
_rate = {}


def _atomic_dump(path, data):
    tmp = path + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(data, f)
    os.replace(tmp, path)


def rate_ok(key, limit, window):
    now = time.time()
    with DATA_LOCK:
        hits = [t for t in _rate.get(key, []) if now - t < window]
        if len(hits) >= limit:
            _rate[key] = hits
            return False
        hits.append(now)
        _rate[key] = hits
        return True


def save_reads(data):
    _atomic_dump(READS_FILE, data)

def load_reactions():
    try:
        with open(REACTIONS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_reactions(data):
    _atomic_dump(REACTIONS_FILE, data)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def fail(self, e):
        msg = repr(e)
        tok = os.getenv('BOT_TOKEN')
        if tok:
            msg = msg.replace(tok, '***')
        print('server error:', msg, file=sys.stderr, flush=True)
        self.send_json(500, {'error': 'internal error'})

    def client_ip(self):
        return (self.headers.get('X-Real-IP') or
                (self.headers.get('X-Forwarded-For') or '').split(',')[0].strip() or
                self.client_address[0])

    def read_body(self, limit=65536):
        try:
            length = int(self.headers.get('Content-Length', 0))
        except ValueError:
            length = 0
        return self.rfile.read(max(0, min(length, limit)))

    def read_json(self):
        try:
            return json.loads(self.read_body() or b'{}')
        except ValueError:
            return {}

    def send_json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/reads':
            self.send_json(200, load_reads())
        elif path == '/reactions':
            self.send_json(200, load_reactions())
        elif path.startswith('/subscription/'):
            uid = path[len('/subscription/'):]
            try:
                conn = sqlite3.connect(DB_FILE)
                row = conn.execute("SELECT expires FROM subscriptions WHERE key=?", (uid,)).fetchone()
                conn.close()
                if row:
                    expires = datetime.fromisoformat(row[0])
                    active = expires > datetime.utcnow()
                    self.send_json(200, {'subscribed': active, 'expires': row[0]})
                else:
                    self.send_json(200, {'subscribed': False})
            except Exception:
                self.send_json(200, {'subscribed': False})
        elif path.startswith('/donate'):
            from urllib.parse import parse_qs
            qs = parse_qs(urlparse(self.path).query)
            try:
                amount = int(qs.get('amount', [0])[0])
            except (ValueError, IndexError):
                amount = 0
            if amount < 1 or amount > 100000:
                self.send_json(400, {'error': 'invalid amount'})
            else:
                try:
                    token = os.getenv('BOT_TOKEN')
                    data = urllib.parse.urlencode({
                        'title': 'Донат автору',
                        'description': 'Поддержка проекта @knigi4bot',
                        'payload': f'donate_{amount}',
                        'currency': 'XTR',
                        'prices': __import__('json').dumps([{'label': 'Донат', 'amount': amount}]),
                    }).encode()
                    req = urllib.request.Request(f'https://api.telegram.org/bot{token}/createInvoiceLink', data=data)
                    resp = urllib.request.urlopen(req, timeout=10)
                    link = __import__('json').loads(resp.read())['result']
                    self.send_json(200, {'link': link})
                except Exception as e:
                    self.fail(e)
        else:
            self.send_json(404, {'error': 'not found'})

    def do_POST(self):
        path = urlparse(self.path).path
        if path.startswith('/read/'):
            book_id = path[len('/read/'):]
            if book_id.isdigit() and len(book_id) <= 6:
                with DATA_LOCK:
                    reads = load_reads()
                    reads[book_id] = reads.get(book_id, 0) + 1
                    save_reads(reads)
                self.send_json(200, {'reads': reads[book_id]})
            else:
                self.send_json(400, {'error': 'missing id'})
        elif path.startswith('/react/'):
            parts = path.split('/')
            if len(parts) == 4:
                book_id, rtype = parts[2], parts[3]
                if rtype in ('up', 'down') and book_id.isdigit() and len(book_id) <= 6:
                  with DATA_LOCK:
                    reactions = load_reactions()
                    if book_id not in reactions:
                        reactions[book_id] = {'up': 0, 'down': 0}
                    reactions[book_id][rtype] = reactions[book_id].get(rtype, 0) + 1
                    save_reactions(reactions)
                    self.send_json(200, reactions[book_id])
                else:
                    self.send_json(400, {'error': 'invalid type'})
            else:
                self.send_json(400, {'error': 'invalid path'})
        elif path == '/suggest':
            body = self.read_json()
            text = str(body.get('text', '')).strip()[:1000] if isinstance(body, dict) else ''
            if text and not rate_ok('suggest:' + self.client_ip(), 5, 3600):
                self.send_json(429, {'error': 'too many requests'})
                return
            if text:
                try:
                    token = os.getenv('BOT_TOKEN')
                    msg = '📚 Предложение книги:\n' + text
                    data = urllib.parse.urlencode({'chat_id': '7308147004', 'text': msg}).encode()
                    req = urllib.request.Request('https://api.telegram.org/bot' + token + '/sendMessage', data=data)
                    urllib.request.urlopen(req, timeout=10)
                    self.send_json(200, {'ok': True})
                except Exception as e:
                    self.fail(e)
            else:
                self.send_json(400, {'error': 'empty'})
        elif path == '/tribute-webhook':
            body_bytes = self.read_body()
            # Verify signature
            api_key = os.getenv('TRIBUTE_API_KEY', '')
            if not api_key:
                self.send_json(403, {'error': 'webhook disabled'})
                return
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
                    # Check existing subscription for renewal
                    import sqlite3 as _sq
                    _conn = _sq.connect(DB_FILE)
                    _row = _conn.execute("SELECT expires FROM subscriptions WHERE key=?", (uid,)).fetchone()
                    _conn.close()
                    if _row and days < 36500:
                        current = datetime.fromisoformat(_row[0])
                        base = max(current, datetime.utcnow())
                    else:
                        base = datetime.utcnow()
                    expires = base + timedelta(days=days)
                    save_subscription_db(uid, expires)
                    try:
                        _c = sqlite3.connect(DB_FILE)
                        _c.execute(
                            "INSERT INTO payments (user_id, username, amount_stars, payload, type) VALUES (?,?,?,?,?)",
                            (int(uid), payload.get('telegram_username', ''), amount, name, 'tribute'))
                        _c.commit()
                        _c.close()
                    except Exception as _e:
                        print('payment log error:', repr(_e), file=sys.stderr, flush=True)
                    # Notify user in Telegram
                    token = os.getenv('BOT_TOKEN')
                    if token and uid:
                        try:
                            exp_str = expires.strftime('%d.%m.%Y') if days < 36500 else 'навсегда'
                            msg = f'✅ Подписка активирована!\n\n📚 Доступ открыт на {period_label}\n📅 Действует до: {exp_str}\n\nОткрой библиотеку: /start'
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
                        msg_admin = f'💳 Оплата картой/криптой\n{display} — {period_label} (${amount})'
                        data = urllib.parse.urlencode({'chat_id': '7308147004', 'text': msg_admin}).encode()
                        req = urllib.request.Request('https://api.telegram.org/bot' + token + '/sendMessage', data=data)
                        urllib.request.urlopen(req, timeout=10)
                    except Exception:
                        pass
                self.send_json(200, {'ok': True})
            except Exception as e:
                self.fail(e)
        else:
            self.send_json(404, {'error': 'not found'})


if __name__ == '__main__':
    port = 5000
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print(f'Server running on port {port}')
    server.serve_forever()
