import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from enums.envs import Env

Base = declarative_base()

DATABASE_URL = Env.POSTGRES_CONNECTION_URL.value

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
