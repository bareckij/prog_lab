import asyncio

async def delayed_message(message: str, delay: float) -> None:
    """Асинхронная функция, которая ждёт `delay` секунд и выводит `message`."""
    await asyncio.sleep(delay)
    print(message)

async def main():
    task1 = asyncio.create_task(delayed_message("Сообщение после 2 секунд", 2))
    task2 = asyncio.create_task(delayed_message("Сообщение после 1 секунды", 1))
    task3 = asyncio.create_task(delayed_message("Сообщение после 3 секунд", 3))

    await asyncio.gather(task1, task2, task3)

    print("Все сообщения выведены!")

# Запускаем main()
asyncio.run(main())