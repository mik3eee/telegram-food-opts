from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters

def main():
    TOKEN = os.environ["TOKEN"]  # Teraz bude fungovať

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("zápis", switch_inline_query_current_chat="zápis: "),
            InlineKeyboardButton("dopyt", switch_inline_query_current_chat="dopyt: "),
        ],
        [
            InlineKeyboardButton("návrh", switch_inline_query_current_chat="návrh: "),
            InlineKeyboardButton("report", switch_inline_query_current_chat="report: "),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Vyberte možnosť – po kliknutí sa text automaticky vyplní a môžete ho doplniť:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Spracovanie ďalších správ (ak je to potrebné)
    await update.message.reply_text(f"Dostal som správu: {update.message.text}")

def main():
    app = Application.builder().token(TOKEN).build()

    # Ak používateľ napíše presne "..", spustí sa funkcia start.
    app.add_handler(MessageHandler(filters.Regex(r"^\.\.$"), start))
    # Ostatné textové správy spracujeme v handle_message
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot beží...")
    app.run_polling()

if __name__ == '__main__':
    main()
