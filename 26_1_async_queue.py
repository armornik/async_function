import asyncio
from random import randint

# Queues - не итерируемый объект (нельзя прокрутить в цикле for, нет индекса)
# Можно получить элемент только из начала очереди, а добавлять только в конец
# Очереди используются как средство коммуникации между корутинами (producer - consumer) (производитель - потребитель)
# producer - тот кто добавляет элемент в очередь
# consumer - тот кто берет элемент из очереди (worker)


class Color:
    norm = '\033[0m'
    blue = '\033[94m'
    green = '\033[92m'


color = Color()


async def producer(queue_async, name):
    timeout = randint(1, 5)
    await queue_async.put(timeout)
    # await asyncio.sleep(timeout)
    print(f'{color.blue}Producer {name} put {timeout} in to queue, {queue_async=} {color.norm}')


async def consumer(queue_async, name):
    # while not queue_async.empty():
    while True:
        timeout = await queue_async.get()
        await asyncio.sleep(timeout)
        print(f'{color.green}Consumer {name} eat {timeout=}, {queue_async=} {color.norm}')
        # task_done() - уменьшает значение количества задач в очереди
        queue_async.task_done()


async def main():
    # maxsize - ограничить очередь максимальным количеством
    queue_async = asyncio.Queue(maxsize=2)
    print(dir(queue_async))

    producers = []

    for i in range(12):
        task = asyncio.create_task(producer(queue_async, name=i))
        producers.append(task)

    consumers = []
    for i in range(4):
        task = asyncio.create_task(consumer(queue_async, name=i))
        consumers.append(task)

    # await asyncio.gather(*producers, *consumers)
    await asyncio.gather(*producers)

    # join - проверяет приватную переменную Queue._unfinished_tasks (есть ли не законченые задачи)
    await queue_async.join()

    # Отменить работу потребителей, которые крутятся в событийном списке, ожидая когда появятся новые элементы
    for c in consumers:
        c.cancel()


if __name__ == '__main__':
    asyncio.run(main())
