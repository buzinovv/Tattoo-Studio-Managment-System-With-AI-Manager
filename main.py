import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from database.db_commands import add_client, get_client
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    telegram_id = message.from_user.id
    
    # Пытаемся найти юзера в базе
    name = await get_client(telegram_id)
    
    if name:
        await message.answer(f"Привет, {name}! Рад видеть тебя снова.")
    else:
        # Если юзера нет, пока что просто добавим его как "Новичок"
        # (Позже сделаем нормальную регистрацию)
        await add_client(telegram_id, message.from_user.first_name)
        await message.answer(f"Привет, {message.from_user.first_name}! Я тебя запомнил.")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())