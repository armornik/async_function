import asyncio


async def greet(timeout):
    await asyncio.sleep(timeout)
    print('Hello world')
    return 'Hello world'


async def main():

    long_task = asyncio.create_task(greet(5))

    try:
        result = await asyncio.wait_for(
            # asyncio.shield - для отправки сообщения пользователю, без остановки корутины
            asyncio.shield(long_task),
            timeout=2
        )

    except asyncio.TimeoutError:
        print('The Task was cancelled')

        result = await long_task
        print(result)


if __name__ == '__main__':
    asyncio.run(main())
