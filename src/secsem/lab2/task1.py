import asyncio

async def delayed_message(message: str, delay: float) -> None:
    """Асинхронная функция, которая ждёт `delay` секунд и выводит `message`."""
    await asyncio.sleep(delay)
    print(message)
async def main():
    print("Начало работы")
    await delayed_message("Сообщение после 2 секунд", 2)
    print("Конец работы")

asyncio.run(main())