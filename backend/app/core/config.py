# backend/app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "dev-secret"  # Default secret key for development purposes
    DATABASE_URL: str = "sqlite:///./test.db"  # Default database URL (can be overridden by environment variable)
    REGISTRATION_SECRET: str = "JBSWY3DPEHPK3PXP"  # Secret key for TOTP (can be overridden by environment variable)

    # Redis settings
    REDIS_HOST: str = "localhost"  # Redis server hostname or IP address
    REDIS_PORT: int = 6379  # Redis server port
    REDIS_DB: int = 0  # Redis database number (default is 0)

    # Load environment variables from the .env file if present
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
