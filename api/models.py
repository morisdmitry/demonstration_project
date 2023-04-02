import re
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, validator, constr


START_FROM_SEVEN = re.compile(r"^7\d*$")
LIMIT_FOR_INITIALS = re.compile(r"^[\u0400-\u04FF\s-]+$")


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowUser(TunedModel):
    name: str
    surname: str
    email: str


class GetUser(BaseModel):
    phone: int


class Userdelete(BaseModel):
    phone: int


class UserCreate(BaseModel):
    name: constr(max_length=50)
    surname: constr(max_length=50)
    patronymic: Optional[constr(max_length=50)]
    phone_number: int = 7000000
    email: Optional[str]
    country: constr(max_length=50)

    @validator("phone_number")
    def validate_phone_number(cls, value):
        if not START_FROM_SEVEN.match(str(value)):
            raise HTTPException(
                status_code=422, detail="Phone number should start with the digit 7"
            )
        return value

    @validator("name", "surname", "patronymic", "country")
    def validate_name(cls, value):
        if not LIMIT_FOR_INITIALS.match(str(value)):
            raise HTTPException(
                status_code=422,
                detail=f"value '{value}' must contain only cyrilic symbols, space and dash",
            )
        return value
