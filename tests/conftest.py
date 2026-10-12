import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-that-is-at-least-32-bytes-long")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.database import get_session
from app.main import app


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def make_auth_headers(client):
    def _make(username: str = "alice", password: str = "password123") -> dict:
        client.post("/auth/register", json={"username": username, "password": password})
        response = client.post(
            "/auth/token", data={"username": username, "password": password}
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _make


@pytest.fixture
def auth_headers(make_auth_headers):
    return make_auth_headers()
