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


async def main():
    # Работает для python 3.11
    async with asyncio.TaskGroup() as tg:
        print(type(tg))
        print(dir(tg))

        res1 = tg.create_task(check('https://youtube.com'))
        res2 = tg.create_task(check('https://google.com'))
        res3 = tg.create_task(check('https://yandex.ru'))

    print(res1.result())
    print(res2.result())
    print(res3.result())


if __name__ == '__main__':
    asyncio.run(main())
