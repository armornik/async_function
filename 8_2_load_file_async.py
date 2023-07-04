import asyncio
import aiohttp  # Для работы с http (так как в asyncio только udp/tcp
from time import time
import os


async def fetch_content(url, session):
    """Функция делающая запрос на сервер - через сессию"""
    # Для работы с сессией используется контекстный менеджер
    # allow_redirects так как предусмотрена переадресация
    async with session.get(url, allow_redirects=True) as response:

        # Получаем картинку
        data = await response.read()

        write_file(data)


def write_file(data):
    """Синхронная функция записывающая файл"""

    # Определяем имя файла для сохранения
    filename = f'file-{int(time() * 1000)}.jpeg'
    if not os.path.exists('file'):
        os.mkdir('file')
    with open(f'file/{filename}', 'wb') as file:
        file.write(data)


async def main():

    # Откуда скачиваем картинки
    url = 'https://loremflickr.com/320/240'

    tasks = []

    # Открываем сессию
    async with aiohttp.ClientSession() as session:

        # Создаем событийный цикл
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        # Выполняем
        # await - предваряет выполнение асинхронной функции
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    t0 = time()
    asyncio.run(main())
    print(time() - t0)
