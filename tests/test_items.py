import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routes.items import _store

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_store():
    _store.clear()
    yield
    _store.clear()


def _create_item(name="Widget", price=9.99) -> dict:
    response = client.post("/items/", json={"name": name, "price": price})
    assert response.status_code == 201
    return response.json()


# ── CREATE ──────────────────────────────────────────────────────────────────


def test_create_item_returns_201():
    response = client.post("/items/", json={"name": "Gadget", "price": 19.99})
    assert response.status_code == 201


def test_create_item_payload():
    response = client.post(
        "/items/", json={"name": "Gadget", "price": 19.99, "in_stock": False}
    )
    data = response.json()
    assert data["name"] == "Gadget"
    assert data["price"] == 19.99
    assert data["in_stock"] is False
    assert "id" in data


def test_create_item_invalid_price():
    response = client.post("/items/", json={"name": "Bad", "price": -5})
    assert response.status_code == 422


def test_create_item_missing_name():
    response = client.post("/items/", json={"price": 5.0})
    assert response.status_code == 422


# ── LIST ────────────────────────────────────────────────────────────────────


def test_list_items_empty():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_items_after_create():
    _create_item("A")
    _create_item("B")
    response = client.get("/items/")
    assert len(response.json()) == 2


# ── GET ─────────────────────────────────────────────────────────────────────


def test_get_item_exists():
    item = _create_item()
    response = client.get(f"/items/{item['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == item["id"]


def test_get_item_not_found():
    response = client.get("/items/nonexistent-id")
    assert response.status_code == 404


# ── UPDATE ──────────────────────────────────────────────────────────────────


def test_update_item():
    item = _create_item()
    response = client.put(
        f"/items/{item['id']}", json={"name": "Updated", "price": 49.99}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"
    assert data["price"] == 49.99


def test_update_item_not_found():
    response = client.put("/items/ghost-id", json={"price": 1.0})
    assert response.status_code == 404


# ── DELETE ──────────────────────────────────────────────────────────────────


def test_delete_item():
    item = _create_item()
    response = client.delete(f"/items/{item['id']}")
    assert response.status_code == 204


def test_delete_item_then_get_returns_404():
    item = _create_item()
    client.delete(f"/items/{item['id']}")
    response = client.get(f"/items/{item['id']}")
    assert response.status_code == 404


def test_delete_item_not_found():
    response = client.delete("/items/ghost-id")
    assert response.status_code == 404
