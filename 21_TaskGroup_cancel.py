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
    try:
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(coro_norm(), name='Coro Norm')
            task2 = tg.create_task(coro_value_error(), name='Coro ValueError')
            task3 = tg.create_task(coro_type_error())
            task4 = tg.create_task(coro_long(), name='Coro Long')

        results = [task1.result(), task2.result(), task3.result(), task4.result()]
        print(results)

    except* ValueError as e:
        print(f'{e=}')
    except* TypeError as e:
        print(f'{e=}')


if __name__ == '__main__':
    asyncio.run(main())
