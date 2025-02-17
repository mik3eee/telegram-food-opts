import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1) Flask aplikácia – pre health check
web_app = Flask(__name__)

@web_app.route("/")
def index():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    web_app.run(host="0.0.0.0", port=port)

# 2) Telegram Bot Handlery
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bot je spustený.")

# Špeciálny handler pre ".."
async def special_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Tu môžeš napríklad poslať inline klávesnicu alebo inú odpoveď
    keyboard = [
        [InlineKeyboardButton("zápis", switch_inline_query_current_chat="zápis: ")],
        [InlineKeyboardButton("dopyt", switch_inline_query_current_chat="dopyt: ")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Vyberte možnosť:", reply_markup=reply_markup)

# Generický handler pre ostatné správy
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Dostal som správu: {update.message.text}")

def run_bot():
    token = os.environ.get("TOKEN")
    if not token:
        raise ValueError("Env premenná TOKEN nie je nastavená.")
    
    app_bot = Application.builder().token(token).build()

    # Pridaj handler pre príkaz /start
    app_bot.add_handler(CommandHandler("start", start))
    # Pridaj špeciálny handler, ktorý zachytí správy presne obsahujúce ".."
    app_bot.add_handler(MessageHandler(filters.Regex(r"^\.\.$"), special_command))
    # Pridaj generický handler pre všetky ostatné textové správy
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot beží...")
    app_bot.run_polling()

# 3) Spúšťací kód
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    run_bot()
