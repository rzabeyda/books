import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, LabeledPrice
from telegram.ext import Application, CommandHandler, ContextTypes, PreCheckoutQueryHandler, MessageHandler, filters, CallbackQueryHandler

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "https://books.zabeyda.lol"
SUBS_FILE = "/root/books/subscriptions.json"
STARS_PRICE = 500  # ~5-6€
SUB_DAYS = 30


def load_subs():
    try:
        with open(SUBS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_subs(data):
    with open(SUBS_FILE, "w") as f:
        json.dump(data, f)


def is_subscribed(user_id: int) -> bool:
    subs = load_subs()
    uid = str(user_id)
    if uid not in subs:
        return False
    expires = datetime.fromisoformat(subs[uid])
    return expires > datetime.utcnow()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    subscribed = is_subscribed(user_id)
    url = f"{WEBAPP_URL}?sub=1" if subscribed else WEBAPP_URL

    keyboard = [
        [InlineKeyboardButton("📚 Открыть библиотеку", web_app=WebAppInfo(url=url))]
    ]
    if not subscribed:
        keyboard.append([InlineKeyboardButton("⭐ Подписка 30 дней — 500 Stars", callback_data="subscribe")])

    markup = InlineKeyboardMarkup(keyboard)
    caption = "Привет! Здесь собраны ключевые идеи лучших книг 📚"
    if subscribed:
        subs = load_subs()
        expires = datetime.fromisoformat(subs[str(user_id)])
        caption += f"\n\n✅ Подписка активна до {expires.strftime('%d.%m.%Y')}"

    try:
        with open("main2.png", "rb") as photo:
            await update.message.reply_photo(photo=photo, caption=caption, reply_markup=markup)
    except FileNotFoundError:
        await update.message.reply_text(caption, reply_markup=markup)


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
    subs = load_subs()
    uid = str(user_id)

    if uid in subs:
        current = datetime.fromisoformat(subs[uid])
        base = current if current > datetime.utcnow() else datetime.utcnow()
    else:
        base = datetime.utcnow()

    expires = base + timedelta(days=SUB_DAYS)
    subs[uid] = expires.isoformat()
    save_subs(subs)

    url = f"{WEBAPP_URL}?sub=1"
    keyboard = [[InlineKeyboardButton("📚 Открыть библиотеку", web_app=WebAppInfo(url=url))]]
    await update.message.reply_text(
        f"✅ Оплата прошла! Подписка активна до {expires.strftime('%d.%m.%Y')}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("subscribe", subscribe_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(PreCheckoutQueryHandler(pre_checkout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
