import graphene
from sqlalchemy.types import Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from postgresdb.connection import Base


class MuscleGroup(graphene.InputObjectType):
    muscle_group_name = graphene.String(required=True)
    muscle_group_image = graphene.String(required=True)

class MuscleGroupModel(Base):
    __tablename__ = "muscle_group"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    muscle_group_name = Column(VARCHAR(length=255), index=True)
    muscle_group_image = Column(VARCHAR(length=255), index=True)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
