from fastapi import FastAPI
from app.database import engine, SessionLocal

from app import models

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from app.routes import health
