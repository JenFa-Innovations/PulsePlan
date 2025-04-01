# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create DB tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (optional cleanup)

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "PulsePlan backend is running 🚀"}
