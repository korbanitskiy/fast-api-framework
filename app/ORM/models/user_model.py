import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.ORM.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    refresh_token = Column(String, unique=True, index=False)
    token = Column(String, unique=True, index=False)
    acc_token_ts = Column(DateTime, default=datetime.datetime.now)
