with open('/root/books/server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Фикс tribute webhook — заменить load_subs на SQLite
old = """                    subs = load_subs()
                    # If renewing, extend from current expiry
                    if uid in subs and days < 36500:
                        current = datetime.fromisoformat(subs[uid])
                        base = max(current, datetime.utcnow())
                    else:
                        base = datetime.utcnow()
                    expires = base + timedelta(days=days)
                    save_subscription_db(uid, expires)"""

new = """                    # Check existing subscription for renewal
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
                    save_subscription_db(uid, expires)"""

content = content.replace(old, new)

with open('/root/books/server.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("server.py fixed")
