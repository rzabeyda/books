with open('/root/books/bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# После WHITELIST проверки добавляем проверку VIP по @username
old_check = '''    if username in WHITELIST and not is_subscribed(user_id):
        subs = load_subs()
        subs[str(user_id)] = (datetime.utcnow() + timedelta(days=36500)).isoformat()
        save_subs(subs)
    subscribed = is_subscribed(user_id)'''

new_check = '''    if username in WHITELIST and not is_subscribed(user_id):
        subs = load_subs()
        subs[str(user_id)] = (datetime.utcnow() + timedelta(days=36500)).isoformat()
        save_subs(subs)
    # Если VIP выдан по @username — переносим на user_id и уведомляем
    if username:
        subs = load_subs()
        ukey = '@' + username.lower()
        if ukey in subs and str(user_id) not in subs:
            expires_str = subs.pop(ukey)
            subs[str(user_id)] = expires_str
            save_subs(subs)
            exp_dt = datetime.fromisoformat(expires_str)
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text="🎉 Вам открыт доступ VIP до " + exp_dt.strftime('%d.%m.%Y') + "!\\n\\nПриятного чтения 📚"
                )
            except Exception:
                pass
    subscribed = is_subscribed(user_id)'''

content = content.replace(old_check, new_check)

with open('/root/books/bot.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
