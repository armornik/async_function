from time import time, sleep


def gen(s: str) -> str:
    """Простой пример генератора"""
    for i in s:
        yield i


def gen2(n: int) -> int:
    """Простой пример генератора"""
    for i in range(n):
        yield i


def gen_filename():
    """Функция создающая имена файлам рандомно"""
    while True:
        pattern = 'file-{}.jpeg'
        t = int(time() * 1000)

        yield pattern.format(str(t))

        print(128)
        yield pattern.format(str(t))
        print(129)


# Создаем объект генератора
g = gen('python')
g2 = gen2(6)

tasks = [g, g2]

# Round Robin (по очереди)
while tasks:
    task = tasks.pop(0)

    try:
        i = next(task)
        print(i)
        # Добавляем наш генератор, если вдруг он не израсходовался
        tasks.append(task)
    except StopIteration:
        pass

g1 = gen_filename()

# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))
#
# print(next(g1))
# sleep(1)
# print(next(g1))
# sleep(1)
# print(next(g1))
# sleep(1)
# print(next(g1))
# sleep(1)
# print(next(g1))
