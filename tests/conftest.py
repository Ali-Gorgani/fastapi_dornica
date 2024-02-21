from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db, Base
from app.main import app

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:110963@localhost:5432/fastapi"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def create_test_user(client):
    user_data = {
        "userName": "testuser",
        "email": "test@example.com",
        "password": "ABcd12!@"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    return response.json()  # Returns the created user data


# Adjust the auth_token fixture to depend on the create_test_user fixture
# This ensures that create_test_user runs first and creates the user
@pytest.fixture(scope="module")
def auth_token(create_test_user, client):
    login_data = {
        "username": "test@example.com",
        "password": "ABcd12!@"
    }
    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    token = response.json().get("access_token")
    return token


@pytest.fixture(scope="function")
def client_with_auth(auth_token, client):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {auth_token}"
    }
    return client
