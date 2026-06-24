import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from database.db_commands import add_client, get_client

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())

class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    name = await get_client(message.from_user.id)
    if name:
        await message.answer(f"Привет, {name}! Мы уже знакомы.")
    else:
        await message.answer("Привет! Давай зарегистрируемся. Как тебя зовут?")
        await state.set_state(Registration.waiting_for_name)

@dp.message(Registration.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Принято! Теперь напиши свой номер телефона.")
    await state.set_state(Registration.waiting_for_phone)

@dp.message(Registration.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data['name']
    phone = message.text
    
    await add_client(message.from_user.id, name, phone)
    
    await message.answer(f"Отлично, {name}! Твой номер {phone} сохранен в системе.")
    await state.clear() 

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())