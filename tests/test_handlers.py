import pytest
from fastapi.testclient import TestClient
from main import app
from config import config


client = TestClient(app)


@pytest.mark.asyncio
async def test_save_user(mongo_db):
    await mongo_db[config.MONGO_DB].records.create_index("phone_number", unique=True)
    item = {
        "name": "иван",
        "surname": "иваниван",
        "patronymic": "иваниваниван",
        "phone_number": 76,
        "email": "string@gmail.com",
        "country": "Россия",
    }

    response = client.post("/save_user_data/", json=item)

    assert response.status_code == 200
    assert response.json()["name"] == item["name"]
    assert response.json()["surname"] == item["surname"]
    assert response.json()["patronymic"] == item["patronymic"]
    assert response.json()["phone_number"] == item["phone_number"]
    assert response.json()["email"] == item["email"]
    assert response.json()["country"] == item["country"]
    collection = mongo_db[config.MONGO_DB]
    assert (
        await collection.records.find_one({"phone_number": item["phone_number"]})
        is not None
    )

    mongo_db.drop_database(config.MONGO_DB)


@pytest.mark.asyncio
async def test_save_user_with_none(mongo_db):
    await mongo_db[config.MONGO_DB].records.create_index("phone_number", unique=True)
    item = {
        "name": "иван",
        "surname": "иваниван",
        "phone_number": 77,
        "country": "Россия",
    }

    response = client.post("/save_user_data/", json=item)

    assert response.status_code == 200
    assert response.json()["name"] == item["name"]
    assert response.json()["surname"] == item["surname"]
    assert response.json()["patronymic"] == None
    assert response.json()["phone_number"] == item["phone_number"]
    assert response.json()["email"] == None
    assert response.json()["country"] == item["country"]
    collection = mongo_db[config.MONGO_DB]
    assert (
        await collection.records.find_one({"phone_number": item["phone_number"]})
        is not None
    )

    mongo_db.drop_database(config.MONGO_DB)


@pytest.mark.asyncio
async def test_update_user(mongo_db):
    await mongo_db[config.MONGO_DB].records.create_index("phone_number", unique=True)
    first_item = {
        "name": "петр",
        "surname": "петрпетр",
        "patronymic": "петрпетрпетр",
        "phone_number": 78,
        "email": "petr@gmail.com",
        "country": "Италия",
    }
    response = client.post("/save_user_data/", json=first_item)

    second_item = {
        "name": "иван",
        "surname": "иваниван",
        "patronymic": "иваниваниван",
        "phone_number": 78,
        "email": "ivan@gmail.com",
        "country": "Россия",
    }
    response = client.post("/save_user_data/", json=second_item)

    assert response.status_code == 200
    assert response.json()["name"] == second_item["name"]
    assert response.json()["surname"] == second_item["surname"]
    assert response.json()["patronymic"] == second_item["patronymic"]
    assert response.json()["phone_number"] == second_item["phone_number"]
    assert response.json()["email"] == second_item["email"]
    assert response.json()["country"] == second_item["country"]
    collection = mongo_db[config.MONGO_DB]
    assert (
        await collection.records.find_one({"phone_number": second_item["phone_number"]})
        is not None
    )

    mongo_db.drop_database(config.MONGO_DB)


@pytest.mark.asyncio
async def test_get_user(mongo_db):
    await mongo_db[config.MONGO_DB].records.create_index("phone_number", unique=True)
    item = {
        "name": "петр",
        "surname": "петрпетр",
        "patronymic": "петрпетрпетр",
        "phone_number": 79,
        "email": "petr@gmail.com",
        "country": "Италия",
    }
    response = client.post("/save_user_data/", json=item)
    phone = {
        "phone_number": 79,
    }
    response = client.post("/get_user_data/", json=phone)
    country_code = 380
    assert response.status_code == 200
    assert response.json()["name"] == item["name"]
    assert response.json()["surname"] == item["surname"]
    assert response.json()["patronymic"] == item["patronymic"]
    assert response.json()["phone_number"] == item["phone_number"]
    assert response.json()["email"] == item["email"]
    assert response.json()["country"] == item["country"]
    assert response.json()["country_code"] == country_code
    collection = mongo_db[config.MONGO_DB]
    assert (
        await collection.records.find_one({"phone_number": item["phone_number"]})
        is not None
    )

    mongo_db.drop_database(config.MONGO_DB)


@pytest.mark.asyncio
async def test_delete_user(mongo_db):
    await mongo_db[config.MONGO_DB].records.create_index("phone_number", unique=True)
    item = {
        "name": "петр",
        "surname": "петрпетр",
        "patronymic": "петрпетрпетр",
        "phone_number": 70,
        "email": "petr@gmail.com",
        "country": "Италия",
    }
    response = client.post("/save_user_data/", json=item)
    phone = {"phone_number": 70}

    response = client.post("/delete_user_data/", json=phone)

    assert response.status_code == 200
    assert response.json()["phone_number"] == item["phone_number"]
    collection = mongo_db[config.MONGO_DB]
    result = await collection.records.find_one({"phone_number": item["phone_number"]})
    assert None == result

    mongo_db.drop_database(config.MONGO_DB)
