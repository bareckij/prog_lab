import asyncio

async def first_function():
    print("Функция 1 - первый print")
    await asyncio.sleep(1)
    print("Функция 1 - второй print")
    await asyncio.sleep(4)
    print("Функция 1 - третий print")

async def second_function():
    print("Функция 2 - первый print")
    await asyncio.sleep(3)
    print("Функция 2 - второй print")
    await asyncio.sleep(1)
    print("Функция 2 - третий print")
    await asyncio.sleep(1)
    print("Функция 2 - четвертый print")

async def main():
    await asyncio.gather(
        first_function(),
        second_function()
    )

# Запускаем event loop
asyncio.run(main())