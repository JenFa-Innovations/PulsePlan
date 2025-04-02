# backend/tests/conftest.py

import pytest
from sqlalchemy import inspect
from app.models import Base
from app.database import get_db, init_engine, engine, SessionLocal
from fastapi.testclient import TestClient
from app.main import create_app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db():
    # Init the test database engine
    init_engine(SQLALCHEMY_TEST_DATABASE_URL)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("📦 Tables in test DB:", inspect(engine).get_table_names())

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db):
    app = create_app()

    app.state.limiter.enabled = False

    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
