import random
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
from flask import Flask, request
import threading

# استيراد الرسائل
from arabic_quotes import quotes, motivational_letters

TOKEN = "8598959396:AAFtoyb6A2emYDzbrO2uxSNzy4Ncxgau1AM"
GROUP_CHAT_ID = -1003328150329  # استبدل بمعرف المجموعة

WEBHOOK_URL = "https://your-render-app.onrender.com/webhook"

app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

async def send_random_message():
    """Select and send a random message."""
    if random.choice([True, False]):
        quote = random.choice(quotes)
        message = f"📝 {quote['text']}\n👤 — {quote['author']}"
    else:
        message = random.choice(motivational_letters)
    
    try:
        await bot_app.bot.send_message(chat_id=GROUP_CHAT_ID, text=message)
        print("Message sent")
    except Exception as e:
        print(f"Error sending message: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is now running via Webhook!")

bot_app.add_handler(CommandHandler("start", start))

@app.route("/webhook", methods=["POST"])
def webhook():
    """Receive updates from Telegram via Webhook."""
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    bot_app.update_queue.put_nowait(update)
    return "OK", 200

@app.route("/")
def home():
    return "Bot is alive!", 200

def run_flask():
    app.run(host="0.0.0.0", port=10000)

def run_bot():
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    # تشغيل Flask والWebhook معًا
    threading.Thread(target=run_flask).start()
    threading.Thread(target=run_bot).start()
    
    # جدولة الرسائل كل ساعة
    import asyncio
    async def schedule_messages():
        while True:
            await send_random_message()
            await asyncio.sleep(3600)
    
    asyncio.run(schedule_messages())
