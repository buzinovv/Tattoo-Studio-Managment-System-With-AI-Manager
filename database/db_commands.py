import asyncpg
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime

# load_dotenv() ищет файл .env и загружает переменные, чтобы os.getenv их видел
load_dotenv()

async def add_client(telegram_id: int, name: str, phone: str = None):
    # Устанавливаем асинхронное соединение
    conn = await asyncpg.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME")
    )
    
    # Запрос с плейсхолдерами $1, $2 — защита от взлома
    query = """
    INSERT INTO clients (telegram_id, name, phone) 
    VALUES ($1, $2, $3) 
    ON CONFLICT (telegram_id) DO UPDATE SET phone = $3
    """
    
    await conn.execute(query, telegram_id, name, phone)
    await conn.close() # Обязательно закрываем, чтобы не забить лимит соединений
    
async def get_client(telegram_id: int):
    conn = await asyncpg.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME")
    )
    
    # Мы ищем ИМЯ пользователя по его TELEGRAM_ID
    query = "SELECT name FROM clients WHERE telegram_id = $1"
    
    # fetchrow вернет строку, если юзер есть, или None, если нет
    row = await conn.fetchrow(query, telegram_id)
    
    await conn.close()
    
    if row:
        return row['name']
    return None

async def add_appointment(telegram_id: int, master_id: int, appointment_date):
    conn = await asyncpg.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME")
    )
    
    query = """
        INSERT INTO appointments (client_id, master_id, appointment_date)
        VALUES (
            (SELECT id FROM clients WHERE telegram_id = $1),
            $2, 
            $3
        )
    """
    
    await conn.execute(query, telegram_id, master_id, appointment_date)
    await conn.close()
