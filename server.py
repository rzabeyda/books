import os
import json
import urllib.request
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

# load .env
_env = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(_env):
    for _line in open(_env):
        _line = _line.strip()
        if _line and '=' in _line and not _line.startswith('#'):
            _k, _v = _line.split('=', 1)
            os.environ.setdefault(_k.strip(), _v.strip())

PLAN_STARS = {'month': 333, 'year': 3333, 'forever': 6667}
PLAN_NAMES = {'month': 'Подписка на месяц', 'year': 'Подписка на год', 'forever': 'Навсегда'}

def create_invoice_link(plan):
    token = os.getenv('BOT_TOKEN')
    stars = PLAN_STARS[plan]
    data = urllib.parse.urlencode({
        'title': PLAN_NAMES[plan],
        'description': 'Полный доступ к библиотеке книг',
        'payload': f'sub_{plan}',
        'currency': 'XTR',
        'prices': json.dumps([{'label': PLAN_NAMES[plan], 'amount': stars}]),
    }).encode()
    req = urllib.request.Request(f'https://api.telegram.org/bot{token}/createInvoiceLink', data=data)
    resp = urllib.request.urlopen(req, timeout=10)
    return json.loads(resp.read())['result']

READS_FILE = '/root/books/reads.json'
SUBS_FILE = '/root/books/subscriptions.json'


def load_subs():
    try:
        with open(SUBS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def load_reads():
    try:
        with open(READS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def save_reads(data):
    with open(READS_FILE, 'w') as f:
        json.dump(data, f)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

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
        elif path.startswith('/subscription/'):
            uid = path[len('/subscription/'):]
            subs = load_subs()
            if uid in subs:
                expires = datetime.fromisoformat(subs[uid])
                active = expires > datetime.utcnow()
                self.send_json(200, {'subscribed': active, 'expires': subs[uid]})
            else:
                self.send_json(200, {'subscribed': False})
        elif path.startswith('/invoice/'):
            plan = path[len('/invoice/'):]
            if plan in PLAN_STARS:
                try:
                    link = create_invoice_link(plan)
                    self.send_json(200, {'link': link})
                except Exception as e:
                    self.send_json(500, {'error': str(e)})
            else:
                self.send_json(400, {'error': 'invalid plan'})
        else:
            self.send_json(404, {'error': 'not found'})

    def do_POST(self):
        path = urlparse(self.path).path
        if path.startswith('/read/'):
            book_id = path[len('/read/'):]
            if book_id:
                reads = load_reads()
                reads[book_id] = reads.get(book_id, 0) + 1
                save_reads(reads)
                self.send_json(200, {'reads': reads[book_id]})
            else:
                self.send_json(400, {'error': 'missing id'})
        else:
            self.send_json(404, {'error': 'not found'})


if __name__ == '__main__':
    port = 5000
    server = HTTPServer(('127.0.0.1', port), Handler)
    print(f'Server running on port {port}')
    server.serve_forever()
