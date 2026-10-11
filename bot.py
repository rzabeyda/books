import os
import sqlite3
import json
import logging
from contextlib import contextmanager
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, PreCheckoutQueryHandler, MessageHandler, filters

load_dotenv()

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO)
# httpx пишет в INFO полный URL запроса вместе с токеном бота — глушим
for _n in ("httpx", "httpcore", "telegram", "apscheduler"):
    logging.getLogger(_n).setLevel(logging.WARNING)
logger = logging.getLogger("books_bot")

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "https://books.zabeyda.lol"
DB_FILE = "/root/books/books.db"
SUB_DAYS = 30

WHITELIST = {'rzabeyda', 'dzabeida', 'azabeyda', 'zzabeyda', 'egosawa', 'nikita493', 'sepa17'}
ADMIN_ID = 7308147004


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_FILE, timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            first_seen TEXT DEFAULT (datetime('now')),
            blocked INTEGER DEFAULT 0
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


def mark_blocked(user_id: int):
    with get_db() as conn:
        conn.execute("UPDATE users SET blocked=1 WHERE user_id=?", (user_id,))
        conn.commit()


def mark_unblocked(user_id: int):
    with get_db() as conn:
        conn.execute("UPDATE users SET blocked=0 WHERE user_id=?", (user_id,))
        conn.commit()


async def safe_send(context, chat_id: int, text: str, **kwargs):
    from telegram.error import Forbidden
    try:
        await context.bot.send_message(chat_id=chat_id, text=text, **kwargs)
        mark_unblocked(chat_id)
    except Forbidden:
        mark_blocked(chat_id)
    except Exception as e:
        logger.warning("safe_send to %s failed: %s", chat_id, type(e).__name__)


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
            "INSERT INTO users (user_id, username, first_name) VALUES (?, ?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET username=excluded.username, first_name=excluded.first_name",
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
    mark_unblocked(user_id)

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
            await safe_send(context, user_id, "🎉 Вам открыт доступ VIP до " + exp_dt.strftime('%d.%m.%Y') + "!\n\nПриятного чтения 📚")

    subscribed = is_subscribed(user_id)
    url = f"{WEBAPP_URL}?sub=1" if subscribed else WEBAPP_URL

    keyboard = [[InlineKeyboardButton("📚 Открыть библиотеку", web_app=WebAppInfo(url=url))]]

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


async def pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payload = update.pre_checkout_query.invoice_payload or ""
    known = {"subscription_30d", "sub_month", "sub_year", "sub_forever"}
    if payload in known or payload.startswith("donate_"):
        await update.pre_checkout_query.answer(ok=True)
    else:
        await update.pre_checkout_query.answer(ok=False, error_message="Неизвестный товар")


async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    payload = update.message.successful_payment.invoice_payload
    stars = update.message.successful_payment.total_amount
    username = (update.effective_user.username or '')

    if payload.startswith('donate_'):
        display = f'@{username}' if username else f'id{user_id}'
        log_payment(user_id, username, stars, payload, 'donate')
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"💛 Донат\n{display} — {stars} ⭐")
        except Exception:
            pass
        await update.message.reply_text("💛 Спасибо за поддержку проекта!")
        return

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
        await update.message.reply_text("Формат: /vip @username 30")
        return
    try:
        days = int(args[1])
    except ValueError:
        await update.message.reply_text("Дни должны быть числом. Пример: /vip @username 30")
        return

    username = args[0].lstrip('@').lower()
    expires = datetime.utcnow() + timedelta(days=days)
    exp_str = expires.strftime('%d.%m.%Y')

    uid = get_user_id_by_username(username)
    if uid:
        set_subscription(str(uid), expires)
        await update.message.reply_text(f"✅ VIP @{username} на {days} дней до {exp_str}")
        await safe_send(context, uid, f"🎉 Вам открыт доступ VIP на {days} дней до {exp_str}!\n\nПриятного чтения 📚")
    else:
        set_subscription('@' + username, expires)
        await update.message.reply_text(
            f"✅ VIP @{username} на {days} дней до {exp_str}\n⚠️ Юзер ещё не открывал бот — уведомление придёт когда зайдёт"
        )


async def blocked_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    with get_db() as conn:
        rows = conn.execute("SELECT user_id, username FROM users WHERE blocked=1").fetchall()
        total = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        blocked = len(rows)
    if not rows:
        await update.message.reply_text("Никто не заблокировал бота 👍")
        return
    lines = [f"🚫 Заблокировали бота: {blocked} из {total}\n"]
    for r in rows:
        name = f"@{r['username']}" if r['username'] else f"id{r['user_id']}"
        lines.append(name)
    await update.message.reply_text("\n".join(lines))


async def payments_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    with get_db() as conn:
        rows = conn.execute(
            "SELECT username, amount_stars, type, paid_at FROM payments ORDER BY paid_at DESC LIMIT 20"
        ).fetchall()
        total = conn.execute("SELECT SUM(amount_stars) FROM payments WHERE type='tribute'").fetchone()[0] or 0
    if not rows:
        await update.message.reply_text("Платежей пока нет")
        return
    lines = [f"💳 Последние платежи (Tribute всего ${total:g}):\n"]
    for r in rows:
        dt = r['paid_at'][:10]
        name = f"@{r['username']}" if r['username'] else 'аноним'
        amt = f"${r['amount_stars']:g}" if r['type'] == 'tribute' else f"{r['amount_stars']} ⭐ ({r['type']})"
        lines.append(f"{dt} | {name} | {amt}")
    await update.message.reply_text("\n".join(lines))



async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    now = datetime.utcnow().isoformat()
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        blocked = conn.execute("SELECT COUNT(*) FROM users WHERE blocked=1").fetchone()[0]
        this_m = conn.execute("SELECT COUNT(*) FROM users WHERE first_seen >= date('now','start of month')").fetchone()[0]
        last_m = conn.execute(
            "SELECT COUNT(*) FROM users WHERE first_seen >= date('now','start of month','-1 month') "
            "AND first_seen < date('now','start of month')").fetchone()[0]
        subs = conn.execute(
            "SELECT COUNT(*) FROM subscriptions WHERE key GLOB '[0-9]*' AND expires > ?", (now,)).fetchone()[0]
        paid = conn.execute("SELECT COUNT(*), COALESCE(SUM(amount_stars),0) FROM payments WHERE type='tribute'").fetchone()
        donates = conn.execute("SELECT COALESCE(SUM(amount_stars),0) FROM payments WHERE type='donate'").fetchone()[0]
    await update.message.reply_text(
        f"📊 Статистика бота\n\n"
        f"👥 Всего юзеров: {total}\n"
        f"🆕 Новых в этом месяце: {this_m}\n"
        f"🆕 Новых в прошлом месяце: {last_m}\n"
        f"🚫 Заблокировали бота: {blocked}\n"
        f"⭐ Активных подписок: {subs}\n"
        f"💳 Оплат через Tribute: {paid[0]} на ${paid[1]:g} (учёт с 11.10.2026)\n"
        f"💛 Донатов: {donates} ⭐"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "📚 /start — открыть библиотеку"
    if update.effective_user.id == ADMIN_ID:
        text += ("\n\nАдмин:\n/stats — статистика\n/vip @user 30 — выдать VIP\n"
                 "/payments — платежи\n/blocked — заблокировавшие")
    await update.message.reply_text(text)


async def error_handler(update, context: ContextTypes.DEFAULT_TYPE):
    from telegram.error import NetworkError, TimedOut
    err = context.error
    if isinstance(err, (NetworkError, TimedOut)):
        logger.warning("Сетевая ошибка Telegram: %s", type(err).__name__)
        return
    logger.error("Необработанная ошибка", exc_info=err)
    msg = f"{type(err).__name__}: {err}"
    if BOT_TOKEN:
        msg = msg.replace(BOT_TOKEN, "***")
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=("⚠️ Ошибка в боте\n" + msg)[:500])
    except Exception:
        pass


async def any_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user:
        return
    user_id = update.effective_user.id
    username = (update.effective_user.username or '').lower()
    first_name = update.effective_user.first_name or ''
    save_user(user_id, username, first_name)
    mark_unblocked(user_id)
    if username:
        exp_dt = transfer_username_sub(username, user_id)
        if exp_dt:
            await safe_send(context, user_id, "🎉 Вам открыт доступ VIP до " + exp_dt.strftime('%d.%m.%Y') + "!\n\nПриятного чтения 📚")

def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vip", vip_command))
    app.add_handler(CommandHandler("payments", payments_command))
    app.add_handler(CommandHandler("blocked", blocked_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_error_handler(error_handler)
    app.add_handler(PreCheckoutQueryHandler(pre_checkout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    app.add_handler(MessageHandler(filters.ALL, any_message_handler))
    print("Бот запущен (SQLite)...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
