# backend/app/main.py

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import Base, engine

limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.routers import auth
    app.include_router(auth.router)
    print("✅ Router /register included")  # Debug check
    Base.metadata.create_all(bind=engine)
    yield

def create_app():
    app = FastAPI(lifespan=lifespan)

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    @app.get("/")
    def root():
        return {"message": "PulsePlan backend is running 🚀"}

    return app
