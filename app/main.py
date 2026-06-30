from fastapi import FastAPI

from app.core.config import settings

from app.database.database import engine, Base

from app.models import warehouse


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)



@app.get("/")
def root():

    return {
        "message":
        "WarehouseMind AI running"
    }



@app.get("/health")
def health():

    return {
        "status":"healthy"
    }