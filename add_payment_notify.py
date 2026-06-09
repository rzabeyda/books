content = open('/root/books/bot.py').read()

old = '''    expires = base + timedelta(days=days)
    subs[uid] = expires.isoformat()
    save_subs(subs)

    url = f"{WEBAPP_URL}?sub=1"
    keyboard = [[InlineKeyboardButton("📚 Открыть библиотеку", web_app=WebAppInfo(url=url))]]
    await update.message.reply_text(
        f"✅ Оплата прошла! Подписка активна до {expires.strftime('%d.%m.%Y')}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )'''

new = '''    expires = base + timedelta(days=days)
    subs[uid] = expires.isoformat()
    save_subs(subs)

    period_label = {30: '1 месяц', 365: '1 год', 36500: 'Навсегда'}.get(days, f'{days} дней')
    exp_str = expires.strftime('%d.%m.%Y') if days < 36500 else 'навсегда'
    username = (update.effective_user.username or '')
    display = f'@{username}' if username else f'id{uid}'
    stars = update.message.successful_payment.total_amount

    # Notify admin
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"⭐ Оплата Stars\\n{display} — {period_label} ({stars} ⭐)"
        )
    except Exception:
        pass

    url = f"{WEBAPP_URL}?sub=1"
    keyboard = [[InlineKeyboardButton("📚 Открыть библиотеку", web_app=WebAppInfo(url=url))]]
    await update.message.reply_text(
        f"✅ Оплата прошла! Подписка активна до {exp_str}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )'''

if old in content:
    content = content.replace(old, new)
    open('/root/books/bot.py', 'w').write(content)
    print('Done')
else:
    print('NOT FOUND')
