import aioredis
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter, Depends, HTTPException
from api.actions import (
    _delete_user_data,
    _get_country_code,
    _get_user_data,
    _save_new_user_data,
    _update_user_data,
)
from api.models import (
    UserResponseSaveUpdate,
    UserCreate,
    GetUserByPhone,
    UserResponseGet,
)
from db.dals import CacheDAO, UserDAO
from db.clients import get_redis, get_mongo

user_crud = APIRouter()


@user_crud.post("/save_user_data/", response_model=UserResponseSaveUpdate)
async def save_user_data(
    body: UserCreate,
    mongo: AsyncIOMotorClient = Depends(get_mongo),
):
    """
    update data if user exists , create data if doesnt exists
    """
    db_mongo = UserDAO(mongo)
    data = await _get_user_data(
        GetUserByPhone(phone_number=body.phone_number), db_mongo
    )
    if data:
        return await _update_user_data(data, body, db_mongo)
    return await _save_new_user_data(body, db_mongo)


@user_crud.post("/get_user_data/", response_model=UserResponseGet)
async def get_user_data(
    body: GetUserByPhone,
    redis: aioredis.Redis = Depends(get_redis),
    mongo: AsyncIOMotorClient = Depends(get_mongo),
):
    db_cache = CacheDAO(redis)
    db_mongo = UserDAO(mongo)

    data = await _get_user_data(body, db_mongo)
    if data:
        country_code = await _get_country_code(data["country"], db_cache)
        data["country_code"] = country_code
        return UserResponseGet(**data)
    raise HTTPException(
        status_code=404, detail=f"User with phone_number {body.phone_number} not found."
    )


@user_crud.post("/delete_user_data/", response_model=GetUserByPhone)
async def delete_user_data(
    body: GetUserByPhone,
    mongo: AsyncIOMotorClient = Depends(get_mongo),
):
    db_mongo = UserDAO(mongo)
    return await _delete_user_data(body, db_mongo)
