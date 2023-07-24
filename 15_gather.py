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

    # Создает группу корутин, все результаты будут собраны в список, в том порядке, в котором передаем
    # return_exceptions - чтобы возвращал результаты ошибок, и работа не прерывалась
    results = await asyncio.gather(
        check('https://youtube.com'),
        check('https://google.com'),
        check('https://yandex.ru'),
        check('https://facebook.com'),
        server_returns_error(),
        return_exceptions=True
    )

    for result in results:
        print(result)

#     Способы передачи через распаковку списка:
    coros = [
        check('https://youtube.com'),
        check('https://google.com'),
        check('https://yandex.ru'),
    ]

    # Для группировки групп с помощью gather - await не используется!!! Ответ в виде списка на каждую группу задач
    group1 = asyncio.gather(
        check('https://youtube.com'),
        check('https://google.com'),
        check('https://yandex.ru'),
    )

    group2 = asyncio.gather(
        check('https://facebook.com'),
        server_returns_error(),
        return_exceptions=True
    )

    groups = asyncio.gather(group2, group1)

    # Ждем выполнения всех корутин в группе
    results22 = await groups

    for result in results22:
        print(result)

    # as_completed - Чтобы получить результаты по мере выполнения (возвращает объект-генератор)
    for coro in asyncio.as_completed(coros):
        result = await coro
        print(result)

    coros2 = [
        check('https://youtube.com'),
        check('https://google.com'),
        check('https://yandex.ru'),
    ]

    results2 = await asyncio.gather(*coros2)

#     Через List comprehension
    urls = ['https://youtube.com',
            'https://google.com',
            'https://yandex.ru'
            ]

    coros2 = [check(url) for url in urls]

    results3 = await asyncio.gather(*coros2)

    results4 = await asyncio.gather(*[check(url) for url in urls])


if __name__ == '__main__':
    asyncio.run(main())
