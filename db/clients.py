from motor.motor_asyncio import AsyncIOMotorClient
import aioredis
from config import config


async def get_mongo():
    client = AsyncIOMotorClient(config.MONGO_URL)
    try:
        yield client[config.MONGO_DB]
    finally:
        client.close()


async def get_redis():
    redis = await aioredis.from_url(config.REDIS_URL)
    try:
        yield redis
    finally:
        await redis.close()
