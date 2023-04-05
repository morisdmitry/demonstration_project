import json
import httpx
from config import config
from api.models import (
    GetUserByPhone,
    UserCreate,
    UserDB,
    UserDeleteByPhone,
    UserResponseSaveUpdate,
)
from db.models import DBUser
from utils import id_generate, timestamp_now

from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError


async def _get_country_code(country, cache):
    cached_value = await cache.get(country)
    if cached_value:
        return int(cached_value.decode("utf-8"))

    async with httpx.AsyncClient() as client:
        url = config.DA_DATA_URL
        api_key = config.DA_DATA_KEY
        secret = config.DA_DATA_SECRET
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {api_key}",
            "X-Secret": f"{secret}",
        }

        query = {"query": country}

        response = await client.post(url, headers=headers, data=json.dumps(query))
        try:
            response.raise_for_status()
            if response.status_code != 200:
                return None
        except Exception as e:
            return None
        country_code = response.json()["suggestions"][0]["data"]["code"]
        await cache.add(country, country_code)
        return country_code


async def _save_new_user_data(body: UserCreate, db_mongo):
    user_data = DBUser(
        user_id=id_generate(12),
        name=body.name,
        surname=body.surname,
        patronymic=body.patronymic,
        phone_number=body.phone_number,
        email=body.email,
        country=body.country,
        date_created=timestamp_now(),
        date_modified=timestamp_now(),
    )
    try:
        await db_mongo.add(json.loads(user_data.json()))
    except DuplicateKeyError as e:
        raise HTTPException(status_code=404, detail=f"DuplicateKeyError {e}")

    return UserResponseSaveUpdate(**json.loads(user_data.json()))


async def _update_user_data(existed_data, body: UserDB, db_mongo):
    body = json.loads(body.json())
    user_data = DBUser(
        user_id=existed_data["user_id"],
        name=body["name"],
        surname=body["surname"],
        patronymic=body["patronymic"],
        phone_number=body["phone_number"],
        email=body["email"],
        country=body["country"],
        date_created=existed_data["date_created"],
        date_modified=timestamp_now(),
    )

    result = await db_mongo.update(
        {"phone_number": user_data.phone_number}, json.loads(user_data.json())
    )
    if result.modified_count > 0:
        return UserResponseSaveUpdate(**json.loads(user_data.json()))
    raise HTTPException(
        status_code=404, detail=f"User with phone_number {body.phone_number} not found."
    )


async def _delete_user_data(body: UserDeleteByPhone, db_mongo):
    delete_user = UserDeleteByPhone(phone_number=body.phone_number)
    result = await db_mongo.delete(json.loads(delete_user.json()))
    if result.deleted_count > 0:
        return GetUserByPhone(phone_number=body.phone_number)
    raise HTTPException(
        status_code=404, detail=f"User with phone_number {body.phone_number} not found."
    )


async def _get_user_data(body: GetUserByPhone, db_mongo):
    data = await db_mongo.get({"phone_number": body.phone_number})
    return data if data else None
