import asyncio


async def greet(message: str):
    print(message + '1')
    await asyncio.sleep(2)
    print(message + '2')


async def main():
    # Посмотреть все Task
    print(asyncio.all_tasks())

    print('-- main beginning')

    # Создаем Task
    asyncio.create_task(greet('text'))

    print(asyncio.all_tasks())

    await asyncio.sleep(1)

    print('-- main finished')

    print(asyncio.all_tasks())


if __name__ == '__main__':
    asyncio.run(main())
