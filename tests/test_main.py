import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, engine
from sqlmodel import SQLModel


@pytest.fixture
def client():
    """Create a test client."""
    SQLModel.metadata.create_all(engine)
    yield TestClient(app)
    SQLModel.metadata.drop_all(engine)


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
