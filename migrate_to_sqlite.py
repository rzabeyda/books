import sqlite3, json
from datetime import datetime

DB = '/root/books/books.db'
conn = sqlite3.connect(DB)

conn.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    first_seen TEXT DEFAULT (datetime('now'))
)''')
conn.execute('''CREATE TABLE IF NOT EXISTS subscriptions (
    key TEXT PRIMARY KEY,
    expires TEXT
)''')
conn.commit()

# Мигрируем subscriptions.json
try:
    subs = json.load(open('/root/books/subscriptions.json'))
    for key, expires in subs.items():
        conn.execute("INSERT OR REPLACE INTO subscriptions (key, expires) VALUES (?, ?)", (key, expires))
    conn.commit()
    print(f"Подписки: {len(subs)} записей перенесено")
except Exception as e:
    print("Ошибка подписок:", e)

# Мигрируем usernames.json
try:
    unames = json.load(open('/root/books/usernames.json'))
    for username, uid in unames.items():
        conn.execute("INSERT OR REPLACE INTO users (user_id, username) VALUES (?, ?)", (uid, username.lower()))
    conn.commit()
    print(f"Юзернеймы: {len(unames)} записей перенесено")
except Exception as e:
    print("Ошибка юзернеймов:", e)

# Мигрируем users.json
try:
    users = json.load(open('/root/books/users.json'))
    for uid in users:
        conn.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (int(uid),))
    conn.commit()
    print(f"Юзеры: {len(users)} записей перенесено")
except Exception as e:
    print("Ошибка юзеров:", e)

# Проверка
rows = conn.execute("SELECT COUNT(*) FROM subscriptions").fetchone()[0]
urows = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
print(f"\nИтого в БД: {rows} подписок, {urows} юзеров")
conn.close()
print("Готово!")
