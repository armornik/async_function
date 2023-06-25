# nc localhost 5000 - подключиться к серверу через терминал

import socket

# selectors.DefaultSelector() - в интерпретаторе  посмотреть функцию, которая хранит объекты, которые мониторятся
import selectors

# Определяем функцию в которой будут храниться
selector = selectors.DefaultSelector()

# Сокет это пара domain:port, черег которые осуществляется взаимодействие между двумя субъектами: клиентом и сервером
# domain:5000


# Определяем серверный сокет
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

    # Регистрируем процессы, за которыми будем наблюдать (серверный сокет)
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    # Обработка полученных пакетов

    # Получить отправленный клиентом пакет
    client_socket, addr = server_socket.accept()
    print('Connection from', addr)

    # Регистрируем процессы, за которыми будем наблюдать (клиентский сокет)
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_massage)


def send_massage(client_socket):
    # Ждем сообщение от пользователя

    # Получить отправленный клиентом пакет
    request = client_socket.recv(4096)

#     Условия выхода из цикла
    if request:
        # ответ пользователю, если есть запрос, закодированный в bytes
        response = 'Hello world./n'.encode()
        # Отправить ответ клиенту
        client_socket.send(response)
    else:
        # Снимает сокет с регистрации перед его закрытием
        selector.unregister(client_socket)

        # Закрываем соединение
        client_socket.close()


def event_loop():
    """Функция, которая управляет событиями (запускает accept_connection при появлении нового пользователя,
    send_massage - когда приходит сообщение от пользователя)"""
    while True:

        # Получаем выборку объектов, которые готовы для чтения или записи
        events = selector.select()  # Возвращает кортеж (key, events) events - битовая маска события (чтение или запись)

        # key - объект класса SelectorKey (namedTuple) именованный кортеж с полями fileobj, events, data

        for key in events:
            # Получаем обратно свою функцию
            callback = key.data

            # Запускаем функцию с нашим сокетом (клиента или серверным)
            callback(key.fileobj)


if __name__ == "__main__":
    server()
    event_loop()
