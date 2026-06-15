import json
from datetime import datetime, timedelta

# 1. Исправить подписку dzabeida на 365 дней
with open('/root/books/subscriptions.json', encoding='utf-8') as f:
    subs = json.load(f)

expires = datetime.utcnow() + timedelta(days=365)
subs['7215817121'] = expires.isoformat()
# Убрать @dzabeida если есть
subs.pop('@dzabeida', None)

with open('/root/books/subscriptions.json', 'w', encoding='utf-8') as f:
    json.dump(subs, f, ensure_ascii=False, indent=2)
print("Подписка dzabeida -> 365 дней до", expires.strftime('%d.%m.%Y'))

# 2. Фиксим bot.py
with open('/root/books/bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Логика переноса: убрать проверку "not in subs" чтобы всегда перезаписывало
old_transfer = "if ukey in subs and str(user_id) not in subs:"
new_transfer = "if ukey in subs:"
content = content.replace(old_transfer, new_transfer)

# Показывать "навсегда" только для whitelist, иначе дату
old_caption = "        caption += f\"\\n\\n✅ Подписка активна до {expires.strftime('%d.%m.%Y')}\""
new_caption = """        days_left = (expires - datetime.utcnow()).days
        if days_left > 3000:
            caption += "\\n\\n✅ Подписка активна навсегда"
        else:
            caption += f"\\n\\n✅ Подписка активна до {expires.strftime('%d.%m.%Y')} (осталось {days_left} дн.)" """
content = content.replace(old_caption, new_caption)

with open('/root/books/bot.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("bot.py обновлён")
