# Dabid Beazley 2015 PyCon "Concurency from the Ground up Live"

import socket

# select(list_1, list_2, list_3) - функция для мониторинга состояния объектов socket. Работает со всеми объектами,
# имеющими метод .fileno() (файловый дискриптор - номер файла). Мониторит изменения в объектах.
# list_1 - первый список, те объекты, за которыми надо наблюдать, когда они станут доступны для чтения
# list_2 - второй список, те объекты, за которыми надо следить, когда они станут доступны для записи
# list_3 - третий список, те объекты, у которых мы ожидаем какие-то ошибки.
# Возвращает списки, когда они станут доступны.
from select import select

# Список для задач
tasks = []

to_read = {}
to_write = {}


def server():
    # Server - субъект
    # server_socket - субъект, который будет принимать запрос
    # AF - глобальная переменная модуля socket, address family (INET - IP V4) (указывающая на IP). Стандартный протокол,
    # разделенный точками на 4 части, по 1 байту на часть.
    # socket.SOCK_STREAM - означает, что речь пойдёт о поддержке протокола TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Убираем таймаут при остановке программы (обычно 1,5 минуты на досылку данных)
    # SOL_SOCKET - уровень на котором устанавливаются опции (SOL - socket level) SOCKET = server_socket (наш сокет)
    # SO_REUSEADDR - допустить повторное использование адреса (SO - socket option)
    # 1 = True (включить)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # связываем субъект с конкретным адресом и портом
    server_socket.bind(('localhost', 5000))

    # Слушать по адресу порт (ожидание пакетов). Слушать входящий буфер на предмет подключений
    server_socket.listen()

    # Обработка полученных пакетов
    while True:

        # Перед блокирующей функцией мы отфутболиваем сокет, откуда был вызван next, функция ставится на паузу, и её
        # выполнение продолжится только тогда, когда socket сможет выполнить функцию без задержек
        yield ('read', server_socket)
        # Получить отправленный клиентом пакет
        client_socket, addr = server_socket.accept()  # read

        print('Connection from', addr)
        # Добавляем функцию client_socket с параметрами сокета
        tasks.append(client(client_socket))


def client(client_socket):
    # Ждем сообщение от пользователя
    while True:

        yield ('read', client_socket)
        # Получить отправленный клиентом пакет
        request = client_socket.recv(4096)  # read

    #     Условия выхода из цикла
        if not request:
            break

    #     ответ пользователю, если есть запрос, закодированный в bytes
        else:
            response = 'Hello world./n'.encode()

            yield ('write', client_socket)
            # Ответить клиенту
            client_socket.send(response)  # write

    # Сообщение на сервер, о том что клиент отключился
    print('Outside inner while loop')
    # Закрываем соединение
    client_socket.close()


# Событийный цикл для управления
def event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            # Наполняем списки значениями ключей (генераторными функциями)
            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            # Получаем кортеж
            task = tasks.pop(0)

            # Распаковываем кортеж
            reason, sock = next(task)

            # В словаре создаём пару: ключ - socket, значение - объект генератора, который остался после вызова next()
            if reason == 'read':
                to_read[sock] = task

            if reason == 'write':
                to_write[sock] = task
        except StopIteration:
            print('Done!')


tasks.append(server())
