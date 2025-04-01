# backend/app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.routers import auth
    app.include_router(auth.router)
    print("✅ Router /register included")  # Debug check
    Base.metadata.create_all(bind=engine)
    yield

def create_app():
    app = FastAPI(lifespan=lifespan)

    @app.get("/")
    def root():
        return {"message": "PulsePlan backend is running 🚀"}

    return app
