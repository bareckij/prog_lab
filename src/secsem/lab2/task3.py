import asyncio

async def delayed_message(message: str, delay: float) -> str:
    """Асинхронная функция, которая ждёт `delay` секунд и возвращает `message`."""
    await asyncio.sleep(delay)
    return message 

async def main():
    tasks = [
        delayed_message("Сообщение после 2 секунд", 2),
        delayed_message("Сообщение после 1 секунды", 1),
        delayed_message("Сообщение после 3 секунд", 3),
    ]

    for completed_task in asyncio.as_completed(tasks):
        result = await completed_task
        print(result)

    print("Все задачи завершены!")

asyncio.run(main())