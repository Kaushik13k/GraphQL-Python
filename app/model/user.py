from sqlalchemy.types import Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column

from postgresdb.connection import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    first_name = Column(VARCHAR(length=255), index=True)
    lastname = Column(VARCHAR(length=255), index=True)
    username = Column(VARCHAR(length=255), index=True)
    email = Column(VARCHAR(length=255), index=True)
    salt = Column(VARCHAR(length=255), index=True)
    hash = Column(VARCHAR(length=255), index=True)
    phone_number = Column(Integer, index=True)
    age = Column(Integer, index=True)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
