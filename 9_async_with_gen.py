# Асинхронность состоит из 2 компонентов:
# 1. Любая конструкция языка, которая способна передавать поток управления программы (генераторы, замыкания, корутины)
# 2. Событийный цикл, который решает какой код будет выполняться

queque = []


def counter():
    count = 0
    while True:
        print(count)
        count += 1

        # В данном случае yield просто передаёт управление
        yield


g = counter()
next(g)
next(g)
next(g)


def printer():
    count = 0
    while True:
        if count % 3 == 0:
            print('Bang!!!')
        count += 1

        yield


# Управление событийным списком
def main():
    while True:
        g = queque.pop(0)
        next(g)
        queque.append(g)


# Создаем событийный список
if __name__ == '__main__':
    g1 = counter()
    queque.append(g1)
    g2 = printer()
    queque.append(g2)

    main()
