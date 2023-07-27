import asyncio

# Для создания фейковых данных
from faker import Faker

# Создаем экземпляр класса Faker, с указанием языка
faker_1 = Faker('en_US')


async def get_user(n=1):
    """Функция для генерации имён"""
    # Чтобы показать, что корутины можно вызывать из асинхронных генераторов
    await asyncio.sleep(0.1)

    for i in range(n):
        # name_male - мужские имена
        fullname = faker_1.name_male().split()
        if len(fullname) != 2:
            print(fullname)
        else:
            name, surname = fullname
        if name:
            yield name, surname


async def main():
    # Генератор словарей list comprehensions
    list_comprehensions = [name async for name in get_user(3)]
    print(list_comprehensions)

    # Генератор словарей dict comprehensions
    dict_comprehensions = {name: surname async for name, surname in get_user(3)}
    print(dict_comprehensions)

    # Генератор множеств set comprehensions
    set_comprehensions = {name async for name in get_user(3)}
    print(set_comprehensions)

if __name__ == '__main__':
    asyncio.run(main())
