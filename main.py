import asyncio
import random
import time
from telegram import Bot

# استيراد القوائم
from arabic_quotes import quotes, motivational_letters

TOKEN = "8598959396:AAFtoyb6A2emYDzbrO2uxSNzy4Ncxgau1AM"
GROUP_CHAT_ID = -1003328150329  # استبدل بمعرف المجموعة الصحيح


async def send_random_message(bot):
    """إرسال رسالة عشوائية إلى المجموعة."""
    if random.choice([True, False]):
        quote = random.choice(quotes)
        message = f"📝 {quote['text']}\n👤 — {quote['author']}"
    else:
        message = random.choice(motivational_letters)

    try:
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=message)
    except Exception as e:
        print(f"Error sending message: {e}")


async def main():
    bot = Bot(token=TOKEN)

    while True:
       await send_random_message(bot)
       time.sleep(3600)  # انتظر ساعة قبل إرسال الرسالة التالية


if __name__ == "__main__":
    asyncio.run(main())
