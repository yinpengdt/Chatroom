import aioredis
import asyncio
import settings


async def get_redis_client():
    return await aioredis.create_redis_pool('redis://127.0.0.1')

vadd0 = get_redis_client()