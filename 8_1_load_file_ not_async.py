import requests
from time import time
import os


def get_file(url):
    # allow_redirects так как предусмотрена переадресация
    response = requests.get(url, allow_redirects=True)
    return response


def write_file(response):
    filename = response.url.split('/')[-1]
    if not os.path.exists('file'):
        os.mkdir('file')
    with open(f'file/{filename}', 'wb') as file:
        file.write(response.content)


def main():
    # Определяем начало работы программы
    t0 = time()

    # Откуда скачиваем картинки
    url = 'https://loremflickr.com/320/240'

    for i in range(10):
        write_file(get_file(url))

    # Засекаем время
    print(time() - t0)


if __name__ == '__main__':
    main()
