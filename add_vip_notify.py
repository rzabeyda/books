with open('/root/books/bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавить USERNAMES_FILE после SUBS_FILE
content = content.replace(
    'SUBS_FILE = "/root/books/subscriptions.json"',
    'SUBS_FILE = "/root/books/subscriptions.json"\nUSERNAMES_FILE = "/root/books/usernames.json"'
)

# 2. Добавить load/save usernames после load/save subs
save_subs_func = '''def save_subs(data):
    with open(SUBS_FILE, "w") as f:
        json.dump(data, f)'''

save_subs_plus = '''def save_subs(data):
    with open(SUBS_FILE, "w") as f:
        json.dump(data, f)

def load_usernames():
    try:
        with open(USERNAMES_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_usernames(data):
    with open(USERNAMES_FILE, "w") as f:
        json.dump(data, f)'''

content = content.replace(save_subs_func, save_subs_plus)

# 3. В start хендлере сохранять username->user_id
old_known = '    known_users = load_users()\n    if str(user_id) not in known_users:'
new_known = '''    # Сохраняем username -> user_id
    if username:
        unames = load_usernames()
        unames[username.lower()] = user_id
        save_usernames(unames)
    known_users = load_users()
    if str(user_id) not in known_users:'''

content = content.replace(old_known, new_known)

# 4. В vip_command добавить отправку сообщения юзеру
old_vip_end = '    await update.message.reply_text("VIP @" + username + " на " + str(days) + " дней до " + exp_str)'
new_vip_end = '''    await update.message.reply_text("VIP @" + username + " на " + str(days) + " дней до " + exp_str)
    # Отправить уведомление юзеру
    unames = load_usernames()
    uid = unames.get(username.lower())
    if uid:
        try:
            await context.bot.send_message(
                chat_id=uid,
                text="🎉 Вам открыт доступ VIP на " + str(days) + " дней до " + exp_str + "!\\n\\nПриятного чтения 📚"
            )
        except Exception:
            await update.message.reply_text("⚠️ Доступ выдан, но уведомить юзера не удалось — возможно он не запускал бот")
    else:
        await update.message.reply_text("⚠️ Доступ выдан, но @" + username + " ещё не запускал бот — уведомление придёт когда зайдёт")'''

content = content.replace(old_vip_end, new_vip_end)

with open('/root/books/bot.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
