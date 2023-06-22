import socket
from views import *

# IP - тоннель между пользователями по которому происходит обмен данными

# tcp - правила по которым передаются данные (порядок получения и отправки покетов ) (дубли убирает, если не хватает -
# делает повторный запрос). port - чтобы несколько приложение могли использовать на одной машине tcp не занимая собой
# весь тоннель

# пара Ip-address:port = socket (гнездо)

URLS = {
    '/': index,
    '/blog': blog
}


def parse_request(request):
    """Функция для распарсивания данных пользователя"""
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return (method, url)


def generate_headers(method, url):
    """Функция для генерации заголовка ответа (для корректной работы в Гугле)"""
    if not method == 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)

    if not url in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)

    return ('HTTP/1.1 200 OK\n\n', 200)


def generate_content(code, url):
    """Функция для генерации тела ответа"""
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'

    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'

    return URLS[url]()


def generate_response(request):
    # Распарсиваем данные. Получаем метод и url пользователя
    method, url = parse_request(request)

    headers, code = generate_headers(method, url)
    body = generate_content(code, url)

    # Кодируем ответ в bytes методом encode()
    return (headers + body).encode()


def run():
    # server_socket - субъект, который будет принимать запрос
    # AF - глобальная переменная модуля socket, address family (INET - IP V4) (указывающая на IP). Стандартный протокол,
    # разделенный точками на 4 части, по 1 байту на часть.
    # socket.SOCK_STREAM - означает, что речь пойдёт о TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Убираем таймаут при остановке программы (обычно 1,5 минуты на досылку данных)
    # SOL_SOCKET - уровень на котором устанавливаются опции (SOL - socket level) SOCKET = server_socket (наш сокет)
    # SO_REUSEADDR - допустить повторное использование адреса (SO - socket option)
    # 1 = True (включить)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # связываем субъект с конкретным адресом и портом
    server_socket.bind(('localhost', 5000))

    # Слушать по адресу порт (ожидание пакетов)
    server_socket.listen()

    # Обработка полученных пакетов
    while True:
        # Получить отправленный клиентом пакет
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        print(request)
        print()
        print(addr)

        # Сгенерировать ответ в зависимости от полученного запроса
        response = generate_response(request.decode('utf-8'))

        # Ответить клиенту
        client_socket.sendall(response)

        # Закрываем соединение (чтобы увидеть ответ в терминале)
        client_socket.close()


if __name__ == '__main__':
    run()
