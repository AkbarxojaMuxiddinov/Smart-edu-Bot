import os
import asyncio
from urllib import response

from dotenv import load_dotenv
from aiogram import Bot,Dispatcher, types, F
from aiogram.filters import Command
import google.generativeai as genai

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3.6-flash')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(
        "Salom! Men sizning AI-o'qituvchingizman.\n"
        "Menga dasturlash bo'yicha kodingizni yoki vazifangizni yuboring, "
        "men uni tekshirib, xatolarini ko'rsataman va baholayman!"
    )




@dp.message(F.text)
async def ai_check_handler(message: types.Message):
    await message.answer("Vazifangiz tekshirilmoqda, biroz kuting...")

    prompt = (
        "Siz dasturlash bo'yicha tajribali o'qituvchisiz. "
        "Quyidagi o'quvchi yuborgan kod yoki vazifani tahlil qiling:\n\n"
        f"{message.text}\n\n"
        "Javobingizda quyidagilar bo'lsin:\n"
        "1. Kod/Vazifa to'g'ri bajarilganmi?\n"
        "2. Xatolar va kamchiliklar (agar bo'lsa).\n"
        "3. Kodni yaxshilash uchun 2 ta maslahat.\n"
        "4. Yakuniy baho (1 dan 10 gacha)."
    )

    try:
        response = model.generate_content(prompt)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")


async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


