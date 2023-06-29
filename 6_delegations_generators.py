from inspect import getgeneratorstate


def coroutines(func):
    """Функция-декоратор, для инициализации генератора"""
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


class BlaBlaException(Exception):
    pass


# Подгенератор (вызываемый генератор)
# @coroutines - если yield from - можно не использовать, так как содержит в себе инициализацию подгенератора
def sub_gen():
    while True:
        try:
            message = yield
        except StopIteration:
            print('Error')
            break
        else:
            print('______', message)
    # Чтобы сработал return, нужно вызвать StopIteration
    return 'Stop!!!'


@coroutines
def delegator(g):
    # while True:
    #     try:
    #         # В делегирующем генераторе перехватываем значения, и передаём их в подгенератор
    #         data = yield
    #         g.send(data)
    #     except BlaBlaException as e:
    #         # Пробрасываем ошибку в подгенератор
    #         g.throw(e)
    result = yield from g
    print(result)


sg = sub_gen()
dg = delegator(sg)
dg.send('While')
dg.send('While2')
dg.send('While3')
# dg.throw(BlaBlaException)
dg.throw(StopIteration)
