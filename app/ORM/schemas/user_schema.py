from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from app.ORM.database import Base
from app.ORM.schemas.base_schema import BaseSchema
from app.ORM.models.user_model import UserModel


class UserValidator(BaseModel):
    """
    Can be used in large applications,
    where separate data input validation is strongly needed
    """
    username: str
    refresh_token: Optional[str]
    token: Optional[str]


class User(UserValidator, BaseSchema):
    id: Optional[int]
    acc_token_ts: Optional[datetime]

    class Config:
        orm_mode = True
        db_model: Base = UserModel
