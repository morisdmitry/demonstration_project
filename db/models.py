from typing import Optional
from pydantic import BaseModel


class CreateDBUser(BaseModel):
    user_id: str
    name: str
    surname: str
    patronymic: Optional[str]
    phone_number: int
    email: Optional[str]
    country: str
    date_created: int
    date_modified: int


class UpdateDBUser(BaseModel):
    user_id: str
    name: str
    surname: str
    patronymic: Optional[str]
    phone_number: int
    email: Optional[str]
    country: str
    date_created: int
    date_modified: int
