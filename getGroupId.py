from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram import Update

TOKEN = "8598959396:AAFtoyb6A2emYDzbrO2uxSNzy4Ncxgau1AM"

async def log_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    print(f"📌 Chat ID = {chat.id}")
    await update.message.reply_text(f"🔢 Chat ID: `{chat.id}`", parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, log_chat_id))

    print("🤖 Bot is running... Send any message in the group to log Chat ID.")
    app.run_polling()

if __name__ == "__main__":
    main()
