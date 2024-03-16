from enum import Enum
import os


class Env(Enum):
    POSTGRES_CONNECTION_URL = os.getenv("POSTGRES_CON_STRING")
    JWT_SECRET = os.getenv("SECRET_KEY")
