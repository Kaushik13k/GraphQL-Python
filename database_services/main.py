import uvicorn
from app import app
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

from app.routes import health

app.include_router(health.router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
