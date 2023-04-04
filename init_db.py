from motor.motor_asyncio import AsyncIOMotorClient
from config import config

client = AsyncIOMotorClient(config.MONGO_URL)
client[config.MONGO_DB].records.create_index("phone_number", unique=True)
