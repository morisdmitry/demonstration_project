from config import config
import asyncio
import pytest
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def mongo_db():
    client = AsyncIOMotorClient(config.MONGO_URL)
    yield client
