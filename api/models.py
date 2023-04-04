import re
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, validator, constr


START_FROM_SEVEN = re.compile(r"^7\d*$")
LIMIT_FOR_INITIALS = re.compile(r"^[\u0400-\u04FF\s-]+$")
EMAIL_VALIDATOR = re.compile("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


class UserResponseSaveUpdate(BaseModel):
    name: str
    surname: str
    patronymic: Optional[str]
    phone_number: int
    email: Optional[str]
    country: str


class UserResponseGet(BaseModel):
    name: str
    surname: str
    patronymic: Optional[str]
    phone_number: int
    email: Optional[str]
    country: str
    country_code: Optional[int]


class GetUserByPhone(BaseModel):
    phone_number: int


class UserDeleteByPhone(BaseModel):
    phone_number: int


class UserCreate(BaseModel):
    name: constr(max_length=50)
    surname: constr(max_length=50)
    patronymic: Optional[constr(max_length=50)]
    phone_number: int
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
    def validate_FIO_and_contry(cls, value):
        if not LIMIT_FOR_INITIALS.match(str(value)):
            raise HTTPException(
                status_code=422,
                detail=f"value '{value}' must contain only cyrilic symbols, space and dash",
            )
        return value

    @validator("email")
    def validate_email(cls, value):
        if not EMAIL_VALIDATOR.match(value):
            raise HTTPException(
                status_code=422,
                detail=f"uncorrect email",
            )
        return value


class UserDB(UserCreate):
    date_created: int
    date_modified: int
