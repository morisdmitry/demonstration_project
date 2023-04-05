from fastapi import APIRouter, FastAPI
import uvicorn
from api.handlers import user_crud
from motor.motor_asyncio import AsyncIOMotorClient
from config import config


app = FastAPI(title="data manager by phone")

main_api_router = APIRouter()
app.include_router(user_crud)


@app.on_event("startup")
async def startup():
    client = AsyncIOMotorClient(config.MONGO_URL)
    await client[config.MONGO_DB].records.create_index("phone_number", unique=True)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


# tests
