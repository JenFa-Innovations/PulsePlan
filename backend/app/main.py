# backend/app/main.py

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import Base, engine
from app.core.config import settings
import redis
from app.core.redis import initialize_redis

# Setup Redis 
redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)

# Initialize Redis client
initialize_redis(redis_client)

# Create limiter with Redis client
limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.routers import auth
    app.include_router(auth.router)
    print("✅ Router /register included")  # Debug check
    Base.metadata.create_all(bind=engine)
    app.state.redis = redis_client  # Store Redis client in app's state
    yield

def create_app():
    app = FastAPI(lifespan=lifespan)

    # Add rate limiting and exception handler for exceeding rate limits
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    @app.get("/")
    def root():
        return {"message": "PulsePlan backend is running 🚀"}

    return app

# Export the app instance so that uvicorn can access it
app = create_app()  # This ensures `uvicorn` can find and run the app instance.