from fastapi import APIRouter
from api.models import ShowUser, UserCreate, GetUser, Userdelete


user_crud = APIRouter()


async def _save_new_user_data(body: UserCreate):
    print(f"_save_new_user_data {body}")
    return ShowUser(name=body.name, surname=body.surname, email=body.email)


async def _delete_user_data(body: Userdelete):
    print(f"delete_user {body}")
    return GetUser(phone=body.phone)


async def _get_user_data(body: Userdelete):
    print(f"get user {body}")
    return GetUser(phone=body.phone)


@user_crud.post("/save_user_data/", response_model=ShowUser)
async def save_user_data(body: UserCreate):
    return await _save_new_user_data(body)


@user_crud.delete("/delete_user_data/", response_model=GetUser)
async def delete_user_data(body: GetUser):
    return await _delete_user_data(body)


@user_crud.post("/get_user_data/", response_model=GetUser)
async def get_user_data(body: GetUser):
    return await _get_user_data(body)
