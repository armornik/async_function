import asyncio
from contextlib import asynccontextmanager
from redis import asyncio as aioredis


@asynccontextmanager
async def redis_connection():
    try:
        redis = await aioredis.from_url('redis://localhost')
        yield redis
    finally:
        await redis.close()


async def main():
    async with redis_connection() as redis:
        await redis.set('course', 'asyncio')

if __name__ == '__main__':
    asyncio.run(main())
