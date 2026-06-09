content = open('/root/books/counter.py').read()

old = '''            if uid in subs and days < 36500:
                current = datetime.fromisoformat(subs[uid])
                base = max(current, datetime.utcnow())
            else:
                base = datetime.utcnow()'''

new = '''            if uid in subs and days < 36500:
                current = datetime.fromisoformat(subs[uid])
                # Only extend from current expiry if it's within 2 years (not whitelist/lifetime)
                if current > datetime.utcnow() and (current - datetime.utcnow()).days < 730:
                    base = current
                else:
                    base = datetime.utcnow()
            else:
                base = datetime.utcnow()'''

if old in content:
    content = content.replace(old, new)
    open('/root/books/counter.py', 'w').write(content)
    print('Done')
else:
    print('NOT FOUND')
