import asyncpg
import os
from dotenv import load_dotenv

# load_dotenv() ищет файл .env и загружает переменные, чтобы os.getenv их видел
load_dotenv()

async def add_client(telegram_id: int, name: str):
    # Устанавливаем асинхронное соединение
    conn = await asyncpg.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME")
    )
    
    # Запрос с плейсхолдерами $1, $2 — защита от взлома
    query = """
    INSERT INTO clients (telegram_id, name) 
    VALUES ($1, $2) 
    ON CONFLICT (telegram_id) DO NOTHING
    """
    
    await conn.execute(query, telegram_id, name)
    await conn.close() # Обязательно закрываем, чтобы не забить лимит соединений