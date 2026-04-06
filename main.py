import asyncio
import aiohttp
from flask import Flask
from telegram import Bot
from config import GROUP_CHAT_ID, TOKEN, OPENROUTER_API_KEY

# ==============================
# إعداد Flask Web Server
# ==============================
app = Flask(__name__)
bot = Bot(token=TOKEN)

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ==============================
# دالة جلب الرسائل من OpenRouter
# ==============================
async def fetch_motivational_message():
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4o-mini",
        "temperature": 0.9,
        "max_tokens": 120,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a creative motivational assistant. Generate short, unique, "
                    "and inspiring messages in Arabic, without mentioning the author. "
                    "Mix motivational, spiritual, knowledge-based, and reflective thoughts. "
                    "Always include relevant emojis. Keep each message under 2 sentences. "
                    "Avoid repeating ideas."
                )
            },
            {
                "role": "user",
                "content": "أعطني رسالة تحفيزية قصيرة ومليئة بالإيموجي."
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=payload) as resp:
            data = await resp.json()
            return data['choices'][0]['message']['content']

# ==============================
# دالة إرسال الرسائل
# ==============================
async def send_message():
    try:
        message = await fetch_motivational_message()
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=message)
    except Exception as e:
        print(f"Error sending message: {e}")

# ==============================
# حلقة asyncio للبوت
# ==============================
async def bot_loop():
    while True:
        await send_message()
        await asyncio.sleep(3600)  # كل ساعة رسالة جديدة

# ==============================
# Endpoint ويب للحفاظ على الخدمة awake
# ==============================
@app.route("/")
def home():
    return "Bot is alive! 😊"

# ==============================
# تشغيل Flask و asyncio معًا
# ==============================
def start_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot_loop())

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    import threading
    t = threading.Thread(target=start_async_loop, args=(loop,))
    t.start()


    # تشغيل Flask
    app.run(host="0.0.0.0", port=10000)