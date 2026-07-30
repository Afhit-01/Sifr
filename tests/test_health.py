import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200


def test_health_payload_shape():
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "healthy"
    assert "app" in data
    assert "version" in data
    assert "environment" in data
    assert "timestamp" in data


def test_readiness_returns_200():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
