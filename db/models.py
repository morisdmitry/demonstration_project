from typing import Optional
from pydantic import BaseModel


class DBUser(BaseModel):
    user_id: str
    name: str
    surname: str
    patronymic: Optional[str]
    phone_number: int
    email: Optional[str]
    country: str
    date_created: int
    date_modified: int
