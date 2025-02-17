import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1) Flask aplikácia – aby sme splnili health check
web_app = Flask(__name__)

@web_app.route("/")
def index():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))  # Render zvyčajne nastaví PORT
    web_app.run(host="0.0.0.0", port=port)

# 2) Telegram Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bot je spustený.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Dostal som správu: {update.message.text}")

def run_bot():
    token = os.environ.get("TOKEN")
    if not token:
        raise ValueError("Env premenná TOKEN nie je nastavená.")
    
    app_bot = Application.builder().token(token).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot beží...")
    app_bot.run_polling()

# 3) Spúšťací kód
if __name__ == "__main__":
    # Spustíme Flask server v samostatnom vlákne
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Spustíme Telegram bota (v hlavnom vlákne)
    run_bot()
