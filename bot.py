import asyncio
import os
import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppData, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

# Используйте переменные окружения для хранения конфиденциальной информации
API_TOKEN = os.getenv('API_TOKEN', '7487635988:AAGvG9Q2NokURLsKsTSg93WQVBnzupFQAxI')
WEBAPP_URL = "https://serenada1.github.io/AcademyInvoker/?v=8"

# Подключение к MongoDB
MONGO_URI = os.getenv('MONGO_URI', "mongodb+srv://AcademyInvoker:<Kostyuch1!>@academyinvoker.h3x9ehr.mongodb.net/?retryWrites=true&w=majority&appName=AcademyInvoker")
client = MongoClient(MONGO_URI)
db = client['mana_bot']
collection = db['progress']

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def load_progress(user_id):
    doc = collection.find_one({"user_id": user_id})
    return doc["progress"] if doc and "progress" in doc else {}

def save_progress(user_id, progress):
    collection.update_one(
        {"user_id": user_id},
        {"$set": {"progress": progress}},
        upsert=True
    )

@dp.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    data: WebAppData = message.web_app_data
    if data:
        raw = data.data.strip()
        if raw:
            try:
                progress = json.loads(raw)
                user_id = str(message.from_user.id)
                save_progress(user_id, progress)
                # Не отправляем сообщение, чтобы не мешать WebApp
            except json.JSONDecodeError:
                await message.answer("Ошибка: не удалось прочитать данные прогресса.")

@dp.message()
async def send_welcome(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть МАНА Бот",
                    web_app={"url": WEBAPP_URL}
                )
            ]
        ]
    )
    await message.answer("Привет! Нажми кнопку ниже, чтобы открыть игру.", reply_markup=keyboard)

async def main():
    print("Бот запущен, ожидаю сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())