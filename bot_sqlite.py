import os
import sqlite3
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, LabeledPrice
from telegram.ext import Application, CommandHandler, ContextTypes, PreCheckoutQueryHandler, MessageHandler, filters, CallbackQueryHandler

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "https://books.zabeyda.lol"
DB_FILE = "/root/books/books.db"
STARS_PRICE = 385
SUB_DAYS = 30

WHITELIST = {'rzabeyda', 'dzabeida', 'azabeyda', 'zzabeyda', 'egosawa', 'nikita493', 'sepa17'}
ADMIN_ID = 7308147004


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
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


def log_payment(user_id: int, username: str, amount_stars: int, payload: str, ptype: str):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO payments (user_id, username, amount_stars, payload, type) VALUES (?,?,?,?,?)",
            (user_id, username, amount_stars, payload, ptype)
        )
        conn.commit()


def is_subscribed(user_id: int) -> bool:
    with get_db() as conn:
        row = conn.execute(
            "SELECT expires FROM subscriptions WHERE key=?", (str(user_id),)
        ).fetchone()
        if not row:
            return False
        return datetime.fromisoformat(row['expires']) > datetime.utcnow()


def get_expires(user_id: int):
    with get_db() as conn:
        row = conn.execute(
            "SELECT expires FROM subscriptions WHERE key=?", (str(user_id),)
        ).fetchone()
        return datetime.fromisoformat(row['expires']) if row else None


def set_subscription(key: str, expires: datetime):
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO subscriptions (key, expires) VALUES (?, ?)",
            (key, expires.isoformat())
        )
        conn.commit()


def transfer_username_sub(username: str, user_id: int):
    """Переносит подписку с @username на user_id"""
    ukey = '@' + username.lower()
    with get_db() as conn:
        row = conn.execute("SELECT expires FROM subscriptions WHERE key=?", (ukey,)).fetchone()
        if row:
            conn.execute("DELETE FROM subscriptions WHERE key=?", (ukey,))
            conn.execute(
                "INSERT OR REPLACE INTO subscriptions (key, expires) VALUES (?, ?)",
                (str(user_id), row['expires'])
            )
            conn.commit()
            return datetime.fromisoformat(row['expires'])
    return None


def get_user_id_by_username(username: str):
    with get_db() as conn:
        row = conn.execute(
            "SELECT user_id FROM users WHERE username=?", (username.lower(),)
        ).fetchone()
        return row['user_id'] if row else None


def save_user(user_id: int, username: str, first_name: str):
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
            (user_id, (username or '').lower(), first_name or '')
        )
        conn.commit()


def is_new_user(user_id: int) -> bool:
    with get_db() as conn:
        row = conn.execute("SELECT 1 FROM users WHERE user_id=?", (user_id,)).fetchone()
        return row is None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = (update.effective_user.username or '').lower()
    first_name = update.effective_user.first_name or ''

    new_user = is_new_user(user_id)
    save_user(user_id, username, first_name)

    if new_user:
        display = f"@{username}" if username else f"id{user_id}"
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"👤 Новый юзер: {display} {first_name}".strip()
            )
        except Exception:
            pass

    if username in WHITELIST and not is_subscribed(user_id):
        set_subscription(str(user_id), datetime.utcnow() + timedelta(days=36500))

    if username:
        exp_dt = transfer_username_sub(username, user_id)
        if exp_dt:
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text="🎉 Вам открыт доступ VIP до " + exp_dt.strftime('%d.%m.%Y') + "!\n\nПриятного чтения 📚"
                )
            except Exception:
                pass

    subscribed = is_subscribed(user_id)
    url = f"{WEBAPP_URL}?sub=1" if subscribed else WEBAPP_URL

    keyboard = [[InlineKeyboardButton("📚 Открыть библиотеку", web_app=WebAppInfo(url=url))]]
    if not subscribed:
        keyboard.append([InlineKeyboardButton("⭐ Подписка 30 дней — 500 Stars", callback_data="subscribe")])

    caption = "Привет! Здесь собраны ключевые идеи лучших книг 📚"
    if subscribed:
        expires = get_expires(user_id)
        days_left = (expires - datetime.utcnow()).days
        if days_left > 3000:
            caption += "\n\n✅ Подписка активна навсегда"
        else:
            caption += f"\n\n✅ Подписка активна до {expires.strftime('%d.%m.%Y')} (осталось {days_left} дн.)"

    try:
        with open("start.jpg", "rb") as photo:
            await update.message.reply_photo(photo=photo, caption=caption, reply_markup=InlineKeyboardMarkup(keyboard))
    except FileNotFoundError:
        await update.message.reply_text(caption, reply_markup=InlineKeyboardMarkup(keyboard))


async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_invoice(update.effective_chat.id, context)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "subscribe":
        await send_invoice(query.message.chat_id, context)


async def send_invoice(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_invoice(
        chat_id=chat_id,
        title="Подписка на 30 дней",
        description="Полный доступ ко всем книгам и идеям на 30 дней",
        payload="subscription_30d",
        currency="XTR",
        prices=[LabeledPrice("Подписка 30 дней", STARS_PRICE)],
        provider_token="",
    )


async def pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    payload = update.message.successful_payment.invoice_payload
    stars = update.message.successful_payment.total_amount
    username = (update.effective_user.username or '')

    days = {'sub_month': 30, 'sub_year': 365, 'sub_forever': 36500, 'subscription_30d': 30}.get(payload, 30)

    expires = get_expires(user_id)
    base = expires if expires and expires > datetime.utcnow() else datetime.utcnow()
    new_expires = base + timedelta(days=days)
    set_subscription(str(user_id), new_expires)

    period_label = {30: '1 месяц', 365: '1 год', 36500: 'Навсегда'}.get(days, f'{days} дней')
    exp_str = new_expires.strftime('%d.%m.%Y') if days < 36500 else 'навсегда'
    display = f'@{username}' if username else f'id{user_id}'

    log_payment(user_id, username, stars, payload, 'stars')

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"⭐ Оплата Stars\n{display} — {period_label} ({stars} ⭐)"
        )
    except Exception:
        pass

    url = f"{WEBAPP_URL}?sub=1"
    keyboard = [[InlineKeyboardButton("📚 Открыть библиотеку", web_app=WebAppInfo(url=url))]]
    await update.message.reply_text(
        f"✅ Оплата прошла! Подписка активна до {exp_str}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def vip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    expires = datetime.utcnow() + timedelta(days=days)
    exp_str = expires.strftime('%d.%m.%Y')

    uid = get_user_id_by_username(username)
    if uid:
        set_subscription(str(uid), expires)
        await update.message.reply_text(f"✅ VIP @{username} на {days} дней до {exp_str}")
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=f"🎉 Вам открыт доступ VIP на {days} дней до {exp_str}!\n\nПриятного чтения 📚"
            )
        except Exception:
            pass
    else:
        set_subscription('@' + username, expires)
        await update.message.reply_text(
            f"✅ VIP @{username} на {days} дней до {exp_str}\n⚠️ Юзер ещё не открывал бот — уведомление придёт когда зайдёт"
        )


async def payments_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    with get_db() as conn:
        rows = conn.execute(
            "SELECT username, amount_stars, type, paid_at FROM payments ORDER BY paid_at DESC LIMIT 20"
        ).fetchall()
        total = conn.execute("SELECT SUM(amount_stars) FROM payments WHERE type='stars'").fetchone()[0] or 0
    if not rows:
        await update.message.reply_text("Платежей пока нет")
        return
    lines = [f"💳 Последние платежи (всего ⭐ {total}):\n"]
    for r in rows:
        dt = r['paid_at'][:10]
        name = f"@{r['username']}" if r['username'] else 'аноним'
        lines.append(f"{dt} | {name} | {r['amount_stars']} ⭐")
    await update.message.reply_text("\n".join(lines))


def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("subscribe", subscribe_command))
    app.add_handler(CommandHandler("vip", vip_command))
    app.add_handler(CommandHandler("payments", payments_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(PreCheckoutQueryHandler(pre_checkout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    print("Бот запущен (SQLite)...")
    app.run_polling()


if __name__ == "__main__":
    main()
