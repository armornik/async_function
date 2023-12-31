#async_function 

##socket - описана работа web-приложения на низком уровне. Сокет и роут.

##original.py - понятие о блокирующих функциях (остановка выполнения программы до получения результата из функции) - постановка проблемы

##1_event_loop.py - создание асинхронности (независимого вызова функций). select - для мониторинга

##2_selectors.py - создание асинхронности (независимого вызова функций). selectors - для мониторинга

##3_generators.py - Примеры генераторов, их возможности и создание Round Robins

##4_async_generators.py - создание асинхронности при помощи генераторных функций

##5_async_coroutines.py - понятие о корутинах (подпрограммах), декоратор

##6_delegations_generators.py - Делегирующий генератор - тот генератор, который вызывает другой генератор. Подгенератор - вызываемый генератор. Когда необходимо разбить один генератор на несколько
Конструкция yield from - управляет работой подгенератора. Можно не использовать инициализацию подгенератора, так как содержит в себе его инициализацию.

##7 Asyncio фреймворк для создания событийных циклов
7_1 - Синтаксис python -V 3.4 (
    обозначение асинхронной функции - декоратор @asyncio.coroutine; 
    предваряет выполнение асинхронной функции (точка входа) - yield from;
    добавляет задачу в очередь событийного цикла - asyncio.ensure_future()
    управляет подгенераторными фукциями (событийный цикл) - asyncio.gather(task_1, task_2)
    создание событийного цикла - loop = asyncio.get_event_loop()
    выполнение программы - loop.run_until_complete(main())
    закрытие программы - loop.close()
)

7_2 - Синтаксис python -V 3.5 (
    обозначение асинхронной функции - async; 
    предваряет выполнение асинхронной функции (точка входа) - await;
    добавляет задачу в очередь событийного цикла - asyncio.ensure_future()
    управляет подгенераторными фукциями (событийный цикл) - asyncio.gather(task_1, task_2)
    создание событийного цикла - loop = asyncio.get_event_loop()
    выполнение программы - loop.run_until_complete(main())
    закрытие программы - loop.close()
)

7_3 - Синтаксис python -V 3.6 (
    обозначение асинхронной функции - async; 
    предваряет выполнение асинхронной функции (точка входа) - await;
    добавляет задачу в очередь событийного цикла - asyncio.create_task()
    управляет подгенераторными фукциями (событийный цикл) - asyncio.gather(task_1, task_2)
    создание событийного цикла - loop = asyncio.get_event_loop()
    выполнение программы - loop.run_until_complete(main())
    закрытие программы - loop.close()
)

7_4 - Синтаксис python -V 3.7+  (
    обозначение асинхронной функции - async; 
    предваряет выполнение асинхронной функции (точка входа) - await;
    добавляет задачу в очередь событийного цикла - asyncio.create_task()
    управляет подгенераторными фукциями (событийный цикл) - asyncio.gather(task_1, task_2)
    asyncio.run(main()) - создание событийного цикла, выполнение и закрытие программы

    ~~создание событийного цикла - loop = asyncio.get_event_loop()~~
    ~~выполнение программы - loop.run_until_complete(main())~~          **УПРАЗНЕНЫ**
    ~~закрытие программы - loop.close()~~
)

##8 Asyncio Пример программы по загрузке файлов

##9 Пример асинхронности на генераторах

##10 Отмена Task по условию cancel() (обработка ошибки asyncio.CancelledError)

##11 Прекращение выполнения корутины (asyncio.wait_for(long_task, timeout=3)) (обработка ошибки asyncio.TimeoutError)

##12 Известить о задержке выполнения программы, но не прекращать (shield)

##13 asyncio.run(def())
1. Создает и запускает Event Loop
2. Создает объект Task из def()
3. Ожидает (await) завершения def()
4. Закрывает Event Loop
У функции run - одна главная задача. Если она выполнится, то все остальные Task отменяются.

##14 asyncio_with Контекстный менеджер асинхронный

##15 gather Создает группу корутин, все результаты будут собраны в список, в том порядке, в котором передаем
return_exceptions - чтобы возвращал результаты ошибок, и работа не прерывалась
Для группировки групп с помощью gather - await не используется!!! Ответ в виде списка на каждую группу задач
as_completed - Чтобы получить результаты по мере выполнения (возвращает объект-генератор)

##16 problems await
1. Await сам по себе не делает переключение на другую корутину, контроль выполнения не отдается в событийный цикл, если результат возвращается сразу (происходит блокировка событийного цикла)

##17 TaskGroup - для Python 3.11

##18 gather exceptions return_exceptions=True

##19 TaskGroup exceptions return_exceptions=True

##20 gather cancel. Для перехвата и обработки используется asyncio.CancelledError
task1 = asyncio.create_task(coro_norm(), name='Coro Norm')
task1.get_name()
task1._state

##21 TaskGroup cancel. Отмена происходит автоматически

##22 async for (iter) (Нужно установить Redis и создать значения таблицы для работы)
1. Метод __aiter__ возвращает объект с __anext__()
2. __anext__() возвращает значение на каждой итерации
3. __anext__() возбуждает исключение StopAsyncIteration

##23 async comprehensions (list, dict, set)
faker - для создания фейковых данных

##24 Не асинхронный контекстный менеджер
@contextmanager - превращает генераторную функцию в контекстный менеджер
Всё что до yield - контекстный менеджер использует как метод __enter__, что после - как метод __exit__

##25 Асинхронный контекстный менеджер
@asynccontextmanager - превращает генераторную функцию в контекстный менеджер
Всё что до yield - контекстный менеджер использует как метод __enter__, что после - как метод __exit__

##26 Асинхронны очереди (Queue)
Queues - не итерируемый объект (нельзя прокрутить в цикле for, нет индекса)
Можно получить элемент только из начала очереди, а добавлять только в конец
Очереди используются как средство коммуникации между корутинами (producer - consumer) (производитель - потребитель)
producer - тот кто добавляет элемент в очередь
consumer - тот кто берет элемент из очереди (worker)
task_done() - уменьшает значение количества задач в очереди
maxsize - ограничить очередь максимальным количеством элементов
join - проверяет приватную переменную Queue._unfinished_tasks (есть ли не законченые задачи)
await queue_async.join()
cancel - отменить работу потребителей, которые крутятся в событийном списке, ожидая когда появятся новые элементы
for c in consumers:
    c.cancel()

##27 Асинхронны очереди (Queue) практический пример

Класс Task (asyncio.Task()) - это обертка вокруг корутины, которая планирует запуск этой корутины в событийном цикле. Так же позволяет отменять корутины, если, например, она выполняется слишком долго (без превращения корутины в задачу, её отменить не получится).