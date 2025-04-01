# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# SQLAlchemy engine for SQLite (can be extended later)
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal for use in dependency injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
