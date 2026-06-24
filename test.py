import asyncio
from database.db_commands import add_client, get_client

async def main():
    # Сначала добавим
    await add_client(123456789, "Тестовый Пользователь")
    
    # Теперь попробуем найти
    name = await get_client(123456789)
    print(f"Найден пользователь: {name}")

if __name__ == "__main__":
    asyncio.run(main())