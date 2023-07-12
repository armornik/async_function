import asyncio


async def greet(timeout):
    await asyncio.sleep(timeout)
    print('Hello world')
    return 'Hello world'


async def main():

    long_task = asyncio.create_task(greet(60))

    try:
        # timeout - через сколько секунд прекратить выполнение корутины
        result = await asyncio.wait_for(long_task, timeout=3)

    except asyncio.TimeoutError:
        print('The Task was cancelled')


if __name__ == '__main__':
    asyncio.run(main())
