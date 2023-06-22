# nc localhost 5000 - подключиться к серверу через терминал

import socket

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

# Обработка полученных пакетов
while True:
    print('Before .accept()')
    # Получить отправленный клиентом пакет
    client_socket, addr = server_socket.accept()
    print('Connection from', addr)

    # Ждем сообщение от пользователя
    while True:
        print('Before .recv()')
        # Получить отправленный клиентом пакет
        request = client_socket.recv(4096)

    #     Условия выхода из цикла
        if not request:
            break

    #     ответ пользователю, если есть запрос, закодированный в bytes
        else:
            response = 'Hello world./n'.encode()

            # Ответить клиенту
            client_socket.send(response)

    # Сообщение на сервер, о том что клиент отключился
    print('Outside inner while loop')
    # Закрываем соединение
    client_socket.close()
