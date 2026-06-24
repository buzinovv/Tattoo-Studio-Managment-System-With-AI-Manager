import asyncio
from database.db_commands import add_client

async def main():
    # Пробуем добавить тестового юзера
    await add_client(123456789, "Тестовый Пользователь")
    print("Пользователь успешно добавлен в БД!")

if __name__ == "__main__":
    asyncio.run(main())