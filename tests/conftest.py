from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.database import get_db, Base
from app.main import app
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:110963@localhost:5432/fastapi"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"userName": "test", "email": "test@test.com", "password": "ABcd12!@"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_listings(test_user, session):
    listings_data = [
        {"type": "HOUSE", "address": "first address", "ownerId": test_user["id"]},
        {"type": "APARTMENT", "address": "second address", "ownerId": test_user["id"]},
        {"type": "NOT_SPECIFIED", "address": "third address", "ownerId": test_user["id"]},
    ]

    def create_listing_model(post):
        return models.Listing(**post)

    listing_map = map(create_listing_model, listings_data)
    session.add_all(list(listing_map))
    session.commit()
    listings = session.query(models.Listing).order_by(models.Listing.id).all()
    return listings
