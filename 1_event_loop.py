# nc localhost 5000 - подключиться к серверу через терминал

import socket

# select(list_1, list_2, list_3) - функция для мониторинга состояния объектов socket. Работает со всеми объектами,
# имеющими метод .fileno() (файловый дискриптор - номер файла). Мониторит изменения в объектах.
# list_1 - первый список, те объекты, за которыми надо наблюдать, когда они станут доступны для чтения
# list_2 - второй список, те объекты, за которыми надо следить, когда они станут доступны для записи
# list_3 - третий список, те объекты, у которых мы ожидаем какие-то ошибки.
# Возвращает списки, когда они станут доступны.
from select import select

to_monitor = []

# Сокет это пара domain:port, черег которые осуществляется взаимодействие между двумя субъектами: клиентом и сервером
# domain:5000

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


def accept_connection(server_socket):
    # Обработка полученных пакетов

    # Получить отправленный клиентом пакет
    client_socket, addr = server_socket.accept()
    print('Connection from', addr)

    # Добавляем сокет клиента в список
    to_monitor.append(client_socket)


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
        # Закрываем соединение
        client_socket.close()


def event_loop():
    """Функция, которая управляет событиями (запускает accept_connection при появлении нового пользователя,
    send_massage - когда приходит сообщение от пользователя)"""
    while True:
        ready_to_read, _, _ = select(to_monitor, [], [])  # read, write, errors

        # обрабатываем полученные сокеты
        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_massage(sock)


if __name__ == "__main__":
    to_monitor.append(server_socket)
    event_loop()
