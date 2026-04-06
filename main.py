import asyncio
import aiohttp
from flask import Flask
from telegram import Bot
from config import GROUP_CHAT_ID, TOKEN, OPENROUTER_API_KEY

app = Flask(__name__)
bot = Bot(token=TOKEN)

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ==============================
# جلب الرسالة من OpenRouter
# ==============================
async def fetch_motivational_message():
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "arcee-ai/trinity-large-preview:free",
        "temperature": 0.9,
        "messages": [
            {"role": "system", "content": (
                "You are a creative motivational assistant. Generate short, unique, "
                "and inspiring messages in Arabic, without mentioning the author. "
                "Mix motivational, spiritual, knowledge-based, and reflective thoughts. "
                "Always include relevant emojis. Keep each message under 2 sentences. "
                "Avoid repeating ideas."
            )},
            {"role": "user", "content": "أعطني رسالة تحفيزية قصيرة ومليئة بالإيموجي."}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=payload) as resp:
            data = await resp.json()
            return data['choices'][0]['message']['content']

# ==============================
# إرسال الرسالة
# ==============================
async def send_message():
    try:
        message = await fetch_motivational_message()
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=message)
        return message
    except Exception as e:
        print(f"Error sending message: {e}")
        return f"Error: {e}"

# ==============================
# Endpoint Flask يرسل رسالة عند زيارة /
# ==============================
@app.route("/")
def home():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    message = loop.run_until_complete(send_message())
    return f"Bot sent message! ✅\n\n{message}"

# ==============================
# تشغيل Flask
# ==============================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)