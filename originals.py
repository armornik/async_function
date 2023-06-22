import socket

# Сокет это пара domain-port, черег которые осуществляется взаимодействие между двумя субъектами: клиентом и сервером
# domain:5000

# Server - субъект
# server_socket - субъект, который будет принимать запрос
# AF - глобальная переменная модуля socket, address family (INET - IP V4) (указывающая на IP). Стандартный протокол,
# разделенный точками на 4 части, по 1 байту на часть.
# socket.SOCK_STREAM - означает, что речь пойдёт о TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
