# backend/app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "dev-secret"
    DATABASE_URL: str = "sqlite:///./test.db"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
