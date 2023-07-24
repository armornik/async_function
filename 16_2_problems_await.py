# 1. Await сам по себе не делает переключение на другую корутину, контроль выполнения не отдается в событийный цикл,
# если результат возвращается сразу (происходит блокировка событийного цикла).

import asyncio


async def busy_loop():
    for i in range(10):
        await nothing()


async def nothing():
    # Чтобы работало нормально, и передавалось управление!!!
    await asyncio.sleep(0)

    print('busy')


async def normal():
    for i in range(10):
        # Чтобы работало нормально, и передавалось управление!!!
        await asyncio.sleep(0)
        print('Normal coroutine')


async def main():

    # Создаем Task
    await asyncio.create_task(busy_loop())
    await asyncio.create_task(normal())
    # await asyncio.gather(
    #     busy_loop(),
    #     normal()
    # )


if __name__ == '__main__':
    asyncio.run(main())
