from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_order_success():
    response = client.get("/orders/ORD-1001")

    assert response.status_code == 200
    assert response.json() == {
        "order_id": "ORD-1001",
        "status": "PENDING",
        "reason": "INVENTORY_NOT_AVAILABLE",
    }


def test_get_order_not_found():
    response = client.get("/orders/ORD-9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}

def test_get_order_without_reason():
    response = client.get("/orders/ORD-1002")

    assert response.status_code == 200
    assert response.json() == {
        "order_id": "ORD-1002",
        "status": "SUBMITTED",
        "reason": None,
    }
