import asyncio
import random
from telegram.ext import Application
from flask import Flask
from arabic_quotes import quotes, motivational_letters

TOKEN = "8598959396:AAFtoyb6A2emYDzbrO2uxSNzy4Ncxgau1AM"
GROUP_CHAT_ID = -1003328150329  # استبدل بمعرف المجموعة

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!", 200  # Endpoint فحص الصحة

async def send_random_messages(application):
    """إرسال رسائل عشوائية إلى المجموعة كل ساعة"""
    while True:
        # اختيار الرسالة عشوائيًا
        if random.choice([True, False]):
            quote = random.choice(quotes)
            message = f"📝 {quote['text']}\n👤 — {quote['author']}"
        else:
            message = random.choice(motivational_letters)

        try:
            await application.bot.send_message(chat_id=GROUP_CHAT_ID, text=message)
            print("Message sent")
        except Exception as e:
            print(f"Error sending message: {e}")

        await asyncio.sleep(3600)  # كل ساعة


async def start_bot():
    application = Application.builder().token(TOKEN).build()
    print("🤖 Bot is running... Sending messages automatically.")
    application.create_task(send_random_messages(application))
    await application.run_polling()


if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: asyncio.run(start_bot())).start()
    app.run(host="0.0.0.0", port=10000)
