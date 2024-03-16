from sqlalchemy import Column, Integer, VARCHAR, LargeBinary
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    first_name = Column(VARCHAR, index=True)
    lastname = Column(VARCHAR, index=True)
    username = Column(VARCHAR, index=True)
    email = Column(VARCHAR, index=True)
    salt = Column(VARCHAR(length=255), index=True)
    hash = Column(VARCHAR(length=255), index=True)
    phone_number = Column(Integer, index=True)
    age = Column(Integer, index=True)

    def __repr__(self):
        return f"<User {self.username}>"


class MuscleGroupModel(Base):
    __tablename__ = "muscle_group"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    muscle_group_name = Column(VARCHAR(length=255), index=True)
    muscle_group_image = Column(VARCHAR(length=255), index=True)

    def __repr__(self):
        return f"<MuscleGroup {self.muscle_group_name}>"
