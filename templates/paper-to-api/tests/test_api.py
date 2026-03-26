"""Smoke tests. Run with: pytest tests/ -v"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "model_name" in data


def test_predict(client):
    resp = client.post("/predict", json={"input": "test"})
    assert resp.status_code == 200
    data = resp.json()
    assert "output" in data


def test_predict_invalid_input(client):
    resp = client.post("/predict", json={})
    assert resp.status_code == 422  # Validation error


def test_docs_available(client):
    resp = client.get("/docs")
    assert resp.status_code == 200
