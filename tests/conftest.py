import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.base import Base
from app.database.session import get_db


# Dedicated test database
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Create all tables before the test session
    and drop them afterwards.
    """
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    """
    Creates a fresh database session for each test.
    """
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db):
    """
    Overrides the application's database dependency
    so every request uses the test database.
    """

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()