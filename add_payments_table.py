import sqlite3, json
from datetime import datetime

DB = '/root/books/books.db'
conn = sqlite3.connect(DB)

# Создаём таблицу payments
conn.execute('''CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    amount_stars INTEGER,
    payload TEXT,
    type TEXT,
    paid_at TEXT DEFAULT (datetime('now'))
)''')
conn.commit()
print("Таблица payments создана")
conn.close()
