import asyncio
from redis import asyncio as aioredis


# Пример итератора не асинхронного
class A:
    def __iter__(self):
        self.x = 0
        return self

    def __next__(self):
        if self.x > 2:
            raise StopIteration
        else:
            self.x += 1
            return self.x


# Пример использования не асинхронного итератора
for i in A():
    print(i)


# Пример асинхронного итератора
class RedisReader:
    # Принимает клиент redis и список ключей которые хочешь получить
    def __init__(self, redis, keys):
        self.redis = redis
        self.keys = keys

    # Получаем итератор списка keys
    def __aiter__(self):
        self.ikeys = iter(self.keys)
        return self

    async def __anext__(self):
        # Получаем ключи
        try:
            key = next(self.ikeys)
        except StopIteration:
            raise StopAsyncIteration

        # Получаем значения из базы
        # client Создает сессию
        async with self.redis.client() as connection:
            name = await connection.get(key)

        return name


async def main():
    redis = await aioredis.from_url('redis://localhost')

    # Ключи, которые нужно получить из redis
    keys = ['red', 'blue', 'dark']

    # Итерируемся через экземпляр класса RedisReader, предварительно передав конструктору
    # переменные класса redis и keys
    async for name in RedisReader(redis, keys):
        print(name)

if __name__ == '__main__':
    asyncio.run(main())
