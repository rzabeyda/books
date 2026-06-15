
vip_code = '''

async def vip_command(update, context):
    from telegram.ext import ContextTypes
    if update.effective_user.id != ADMIN_ID:
        return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Формат: /vip 30 @username")
        return
    try:
        days = int(args[0])
    except ValueError:
        await update.message.reply_text("Дни должны быть числом. Пример: /vip 30 @username")
        return
    username = args[1].lstrip('@').lower()
    subs = load_subs()
    matched_uid = None
    for uid, val in subs.items():
        if uid.lstrip('@').lower() == username:
            matched_uid = uid
            break
    if not matched_uid:
        matched_uid = '@' + username
    expires = datetime.utcnow() + timedelta(days=days)
    subs[matched_uid] = expires.isoformat()
    save_subs(subs)
    exp_str = expires.strftime('%d.%m.%Y')
    await update.message.reply_text("VIP @" + username + " на " + str(days) + " дней до " + exp_str)
'''

with open('/root/books/bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Insert function before def main()
content = content.replace('def main():', vip_code + '\ndef main():')

# Add handler inside main()
content = content.replace(
    'app.add_handler(CommandHandler("subscribe", subscribe_command))',
    'app.add_handler(CommandHandler("subscribe", subscribe_command))\n    app.add_handler(CommandHandler("vip", vip_command))'
)

with open('/root/books/bot.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
