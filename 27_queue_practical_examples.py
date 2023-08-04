import asyncio
import aiohttp
from bs4 import BeautifulSoup

# Так как сохранение картинки - блокирующая фунцкция, используем библиотеку
import aiofiles

# ProcessPoolExecutor - поддерживает протокол контекстных менеджеров
from concurrent.futures import ProcessPoolExecutor


async def make_request(url, session):
    """Корутина, которая делает запрос к серверу"""
    response = await session.get(url)

    if response.ok:
        return response
    else:
        print(f'{url} returned: {response.status}')


async def get_image_page(queue, session):
    """Функция, которая получает номера редиректных страниц"""
    url = 'https://c.xkcd.com/random/comic/'

    response = await make_request(url, session)

    # Ответ от сервера кладем в очередь (редирект)
    await queue.put(response.url)


def _parse_link(html):
    soup = BeautifulSoup(html, 'lxml')

    # Находим нужную ссылку
    image_link = 'https:' + soup.select_one('div#comic>img').get('src')
    return image_link


async def get_image_url(pages_queue, image_urls_queue, session):
    while True:
        # Получаем url из очереди
        url = await pages_queue.get()

        # Делаем запрос по url
        response = await make_request(url, session)

        # Получаем html страницы
        html = await response.text()

        # Чтобы делать дальнейшую обработку, создаем отдельный поток для синхронных функций
        # Для этого получаем текущий событийный список
        loop = asyncio.get_running_loop()
        # Создаем экземпляр класса ProcessPoolExecutor
        with ProcessPoolExecutor() as pool:
            # Чтобы запустить нужную синхронную функцию в отдельном процессевызываем
            image_link = await loop.run_in_executor(
                pool,  # Процесс или поток в котором мы хотим запускать
                _parse_link,  # Функция, которая будет выполняться
                html  # Все аргументы, которые нужны для работы  _parse_link
            )

        # После получения ссылки страницы, помещаем ее в очередь image_urls_queue
        await image_urls_queue.put(image_link)

        # Уменьшаем задачу на 1
        pages_queue.task_done()


async def download_image(queue, session):
    while True:
        url = await queue.get()

        response = await make_request(url, session)

        filename = url.split('/')[-1]

        # Сохраняем файл частями по 1024 байта
        async with aiofiles.open(filename, 'wb') as f:
            async for chunk in response.content.iter_chunked(1024):
                await f.write(chunk)

        queue.task_done()


def cancel_tasks(tasks):
    """Отменить работу потребителей, которые крутятся в событийном списке, ожидая когда появятся новые элементы"""
    [task.cancel() for task in tasks]


def create_tasks(number_of_workers: int, coro, *args):
    tasks = []
    for _ in range(number_of_workers):
        task = asyncio.create_task(coro(*args))

        tasks.append(task)

    return tasks

    # return [asyncio.create_task(coro(*args)) for _ in range(number_of_workers)]


async def main():
    session = aiohttp.ClientSession()

    # Создаем объект очереди, в котором будут храниться ссылки на страницы
    pages_queue = asyncio.Queue()
    image_urls_queue = asyncio.Queue()

    page_getters = create_tasks(4, get_image_page, pages_queue, session)
    # page_getters = []
    # for i in range(4):
    #     # Создаем объект класса Task
    #     task = asyncio.create_task(
    #         get_image_page(pages_queue, session)
    #     )
    #
    #     page_getters.append(task)

    url_getters = create_tasks(4, get_image_url, pages_queue, image_urls_queue, session)
    # url_getters = []
    # for i in range(4):
    #     # Создаем объект класса Task
    #     task = asyncio.create_task(
    #         get_image_url(pages_queue, image_urls_queue, session)
    #     )
    #
    #     url_getters.append(task)

    await asyncio.gather(*page_getters)

    # join - проверяет приватную переменную Queue._unfinished_tasks (есть ли не законченые задачи)
    await pages_queue.join()

    # Отменить работу потребителей, которые крутятся в событийном списке, ожидая когда появятся новые элементы
    # for task in page_getters:
    #     task.cancel()
    cancel_tasks(page_getters)

    print(image_urls_queue)

    # Создаем несколько задач для скачивания картинок
    downloaders = create_tasks(4,  download_image, image_urls_queue, session)
    # downloaders = []
    # for i in range(4):
    #     # Создаем объект класса Task
    #     task = asyncio.create_task(
    #         download_image(image_urls_queue, session)
    #     )
    #
    #     downloaders.append(task)

    await image_urls_queue.join()

    # for task in downloaders:
    #     task.cancel()
    cancel_tasks(downloaders)

    await session.close()

if __name__ == '__main__':
    asyncio.run(main())
