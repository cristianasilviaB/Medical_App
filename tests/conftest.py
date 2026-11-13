import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
import model
from main import app
import os

## Test Configuration
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://medical_user:medical_password@localhost:5432/hospital_test_db"
)

admin_url = TEST_DATABASE_URL.rsplit("/", 1)[0] + "/postgres"
admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
with admin_engine.connect() as conn:
    exists = conn.execute(
        text("SELECT 1 FROM pg_database WHERE datname = 'hospital_test_db'")
    ).scalar()
    if not exists:
        conn.execute(text("CREATE DATABASE hospital_test_db"))
admin_engine.dispose()

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()