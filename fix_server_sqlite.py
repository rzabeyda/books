with open('/root/books/server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Добавить sqlite3 import
content = content.replace('import os\nimport json', 'import os\nimport json\nimport sqlite3')

# Добавить DB_FILE константу
content = content.replace(
    "PLAN_STARS = ",
    "DB_FILE = '/root/books/books.db'\n\nPLAN_STARS = "
)

# Добавить функцию is_subscribed_db после load_subs
old_load_subs = """def load_subs():
    try:
        with open(SUBS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}"""

new_load_subs = """def load_subs():
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
        pass"""

content = content.replace(old_load_subs, new_load_subs)

# Заменить проверку подписки в /subscription/ эндпоинте на SQLite
old_sub_check = """        elif path.startswith('/subscription/'):
            uid = path[len('/subscription/'):]
            subs = load_subs()
            if uid in subs:
                expires = datetime.fromisoformat(subs[uid])
                active = expires > datetime.utcnow()
                self.send_json(200, {'subscribed': active, 'expires': subs[uid]})
            else:
                self.send_json(200, {'subscribed': False})"""

new_sub_check = """        elif path.startswith('/subscription/'):
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
                self.send_json(200, {'subscribed': False})"""

content = content.replace(old_sub_check, new_sub_check)

# Заменить tribute webhook сохранение подписки на SQLite
old_save = "                    subs[uid] = expires.isoformat()\n                    save_subs(subs)"
new_save = "                    save_subscription_db(uid, expires)"
content = content.replace(old_save, new_save)

with open('/root/books/server.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
