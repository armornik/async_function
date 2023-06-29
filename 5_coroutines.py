from inspect import getgeneratorstate


def coroutines(func):
    """Функция-декоратор, для инициализации генератора"""
    def inner(*args, **kwargs):
        g1 = func(*args, **kwargs)
        g1.send(None)
        return g1

    return inner


@coroutines
def sub_gen():
    x = 'Ready to accept message'
    message = yield x
    print('Sub_gen received:', message)


try:
    g = sub_gen()
    # g.send('asdf') - ошибка. Вначале нужно передать None!!!
    # Смотрим состояние генератора (GEN_CREATED)
    print(getgeneratorstate(g))

    # Передаем None - управление сдвикается до следующего yield (как при работе с функцией Next
    print(g.send(None))  # Ready to accept message
    # Проверяем состояние генератора (GEN_SUSPENDED) - генератор приостановлен
    print(getgeneratorstate(g))
    print(type(g))

    g.send('Ok')  # Sub_gen received: Ok
except StopIteration:
    pass


class BlaBlaException(Exception):
    pass


@coroutines
def average():
    count = 0
    summa = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print('Done')
            break
        except BlaBlaException:
            print('___________________')
            break
        else:
            count += 1
            summa += x
            average = round(summa / count, 2)

    return average


g = average()
# print(g.send(None))
print(getgeneratorstate(g))
print(g.send(1))
print(g.send(2))
print(g.send(3))

# Вызываем исключение
try:
    g.throw(StopIteration)
except StopIteration as e:
    print('Average', e.value)


# print(g.send(3))

# # Вызываем исключение
# try:
#     g.throw(BlaBlaException)
# except BlaBlaException as e:
#     print('Average', e.value)
