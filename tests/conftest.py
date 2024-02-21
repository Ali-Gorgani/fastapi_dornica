import uuid

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db, Base
from app.main import app
from app.models import User, Listing

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:110963@localhost:5432/fastapi_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)  # Create schema for testing


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def reset_test_db():
    # Establish a new session
    db = TestingSessionLocal()
    try:
        # Delete data from specific tables
        db.query(User).delete()
        db.query(Listing).delete()
        # Add other tables as needed

        # Commit changes
        db.commit()
    except Exception as e:
        print(f"Failed to reset test database: {e}")
        db.rollback()
    finally:
        db.close()


@pytest.fixture(scope="module")
def create_test_user():
    # # Optional: Reset database state before creating a new test user
    # reset_test_db()

    # Generate a unique username and email for each test run
    unique_suffix = str(uuid.uuid4())[:8]  # Generate a random UUID and use the first 8 characters
    user_data = {
        "userName": f"testuser_{unique_suffix}",
        "email": f"test_{unique_suffix}@example.com",
        "password": "ABcd12!@"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201, response.text
    return response.json()  # Returns the created user data


@pytest.fixture(scope="module")
def auth_token(create_test_user):
    login_data = {
        "username": "test@example.com",
        "password": "ABcd12!@"
    }
    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    return token


@pytest.fixture(scope="function")
def client_with_auth(auth_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {auth_token}"
    }
    return client
