import asyncio

# Queues - не итерируемый объект (нельзя прокрутить в цикле for, нет индекса)
# Можно получить элемент только из начала очереди, а добавлять только в конец
# Очереди используются как средство коммуникации между корутинами (producer - consumer) (производитель - потребитель)
# producer - тот кто добавляет элемент в очередь
# consumer - тот кто берет элемент из очереди (worker)


async def add_elem(queue_async, somebody):
    await queue_async.put(somebody)
    print(queue_async)
    return queue_async


async def get_elem(queue_async):
    elem_from_queue = await queue_async.get()
    print(elem_from_queue)
    return elem_from_queue


async def main():
    queue_async = asyncio.Queue()

    print(dir(queue_async))

    task1 = asyncio.create_task(add_elem(queue_async, 2))
    task2 = asyncio.create_task(add_elem(queue_async, [2, 5, 6]))
    task3 = asyncio.create_task(get_elem(queue_async, ))
    task4 = asyncio.create_task(add_elem(queue_async, [2, 5, 6]))
    task5 = asyncio.create_task(get_elem(queue_async, ))
    task6 = asyncio.create_task(add_elem(queue_async, 2))

    tasks = [task1, task2, task3, task4, task5, task6]

    results = await asyncio.gather(*tasks)

    # print(results)

if __name__ == '__main__':
    asyncio.run(main())
