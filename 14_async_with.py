import asyncio
import aiohttp


class WriteToFile:
    def __init__(self, filename):
        """Принимет имя файла"""
        self.filename = filename

    def __enter__(self):
        """Возвращает контекст (файловый объект)"""

#         Сохраняем в атрибут file_object
        self.file_object = open(self.filename, 'w')
        return self.file_object

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_object:
            self.file_object.close()


with WriteToFile('test.txt') as f:
    f.write('Hello')


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


async def check(url):
    async with AsyncSession(url) as response:
        # Дожидаемся ответа и получаем его
        html = await response.text()
        print(f'{url}: {html[:20]}')


async def main():

    # Создаем Task
    # await asyncio.create_task(check('https://facebook.com'))
    res3 = asyncio.create_task(check('https://youtube.com'))
    res2 = asyncio.create_task(check('https://google.com'))
    res1 = asyncio.create_task(check('https://yandex.ru'))

    print(await res1)
    print(await res2)
    print(await res3)


if __name__ == '__main__':
    asyncio.run(main())
