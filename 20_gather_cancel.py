import asyncio
import aiohttp


class AsyncSession:
    def __init__(self, url):
        """Принимет url"""
        self.url = url

    async def __aenter__(self):
        # Создаем объект сессии
        self.session = aiohttp.ClientSession()
        response = await self.session.get(self.url)
        return response

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()


class ServerError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


async def server_returns_error():
    await asyncio.sleep(2)

    raise ServerError('Error on servers')


async def check(url):
    async with AsyncSession(url) as response:
        # Дожидаемся ответа и получаем его
        html = await response.text()
        return f'{url}: {html[:20]}'


async def coro_norm():
    return 'Hello world'


async def coro_value_error():
    raise ValueError


async def coro_type_error():
    raise TypeError


async def coro_long():
    try:
        print('Long task is running...')
        await asyncio.sleep(2)
        print('Long task is finished')
        return 'Long task'

    except asyncio.CancelledError as e:
        print('All needed actions are done')
        raise asyncio.CancelledError


async def main():
    task1 = asyncio.create_task(coro_norm(), name='Coro Norm')
    task2 = asyncio.create_task(coro_value_error(), name='Coro ValueError')
    task3 = asyncio.create_task(coro_type_error())
    task4 = asyncio.create_task(coro_long(), name='Coro Long')

    tasks = [task1, task2, task3, task4]
    try:
        results = await asyncio.gather(*tasks)
    except ValueError as e:
        print(f'{e=}')
    except TypeError as e:
        print(f'{e=}')
    else:
        print(f'{results=}')

    for task in tasks:
        if task.done() is False:
            task.cancel()
            # Какие задачи в ожидании
            print(f'Pending: {task.get_name()}')
        else:
            print(f'Finished: {task.get_name()}')

    print()

    await asyncio.sleep(3)
    print(f'{task1.get_name(), task1._state}')
    print(f'{task2.get_name(), task2._state}')
    print(f'{task3.get_name(), task3._state}')
    print(f'{task4.get_name(), task4._state}')

if __name__ == '__main__':
    asyncio.run(main())
