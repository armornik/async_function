# План
# 1. Asyncio фреймворк для создания событийных циклов
# 2. Пример простой асинхроннной программы времён Python 3.4
# 3. Синтаксис Async/await на замену @asyncio.coroutine и yield from
# 4. Пример асинхронного скачивания файлов
# Event Loop:
#     coroutine > Task (Future)

import asyncio


async def print_nums():
    """Генераторная Функция печатающая числа от 0 до бесконечности"""
    num = 1
    while True:
        print(num)
        num += 1
        await asyncio.sleep(1)


async def print_time():
    """Генераторная Функция определяющая сколько прошло времени с начала цикла"""
    count = 0
    while True:
        if count % 3 == 0:
            print(f'{count} seconds have passed')
        count += 1
        await asyncio.sleep(1)


async def main():
    """Генераторная Функция определяющая работу подгенераторных функций (событийный цикл)"""
    # ensure_future - добавляет задачу в очередь событийного цикла
    task_1 = asyncio.ensure_future(print_nums())
    task_2 = asyncio.ensure_future(print_time())

    # gather - управляет подгенераторными фукциями (событийный цикл)
    await asyncio.gather(task_1, task_2)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
