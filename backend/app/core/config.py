# backend/app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "dev-secret"
    DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"

settings = Settings()
