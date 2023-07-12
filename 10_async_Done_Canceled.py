import asyncio


async def coro():
    return 1


async def greet(timeout):
    await asyncio.sleep(timeout)
    print('Hello world')
    return 'Hello world'


async def main():
    task = asyncio.create_task(coro())

    await task

    # Проверяем была ли задача выполнена успешно
    print(task.done())

    # Проверяем была ли задача отменена
    print(task.cancelled())

    # Выводим список методов
    print(dir(task))

    long_task = asyncio.create_task(greet(60))

    seconds = 0
    while not long_task.done():
        await asyncio.sleep(1)
        seconds += 1

        if seconds == 5:
            # Вызываем отмену Task по условию
            long_task.cancel()

        print('Time passed', seconds)

    try:
        await long_task

    except asyncio.CancelledError:
        print('The Task was cancelled')


if __name__ == '__main__':
    asyncio.run(main())
