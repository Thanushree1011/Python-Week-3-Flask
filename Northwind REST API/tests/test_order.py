
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def sample_order():
    return SimpleNamespace(
        id=10,
        employee_id=2,
        customer_id=4,
        order_date=None,
        shipped_date=None,
        shipper_id=None,
        ship_name="Test Customer",
        ship_address="123 Test Street",
        ship_city="Bengaluru",
        ship_state_province=None,
        ship_zip_postal_code=None,
        ship_country_region="India",
        shipping_fee=50,
        taxes=10,
        payment_type="Cash",
        paid_date=None,
        notes="Test order",
        tax_rate=None,
        tax_status_id=None,
        status_id=None
    )


def test_get_all_orders(client):
    order = sample_order()

    with patch(
        "app.routes.order_routes.get_all_orders",
        return_value=[order]
    ):
        response = client.get("/orders")

    assert response.status_code == 200
    assert len(response.json["orders"]) == 1
    assert response.json["orders"][0]["id"] == 10


def test_get_order_by_id(client):
    order = sample_order()

    with patch(
        "app.routes.order_routes.get_order_by_id",
        return_value=order
    ):
        response = client.get("/orders/10")

    assert response.status_code == 200
    assert response.json["order"]["id"] == 10
    assert response.json["order"]["customer_id"] == 4


def test_order_not_found(client):
    with patch(
        "app.routes.order_routes.get_order_by_id",
        return_value=None
    ):
        response = client.get("/orders/9999")

    assert response.status_code == 404
    assert response.json["error"] == "Order not found"


def test_create_order(client):
    order = sample_order()

    with patch(
        "app.routes.order_routes.create_order",
        return_value=order
    ):
        response = client.post(
            "/orders",
            json={
                "employee_id": 2,
                "customer_id": 4,
                "ship_name": "Test Customer",
                "ship_city": "Bengaluru",
                "payment_type": "Cash"
            }
        )

    assert response.status_code == 201
    assert response.json["message"] == "Order created successfully"
    assert response.json["order"]["id"] == 10


def test_update_order(client):
    order = sample_order()
    order.ship_city = "Mysuru"
    order.notes = "Updated test order"

    with patch(
        "app.routes.order_routes.update_order",
        return_value=order
    ):
        response = client.put(
            "/orders/10",
            json={
                "ship_city": "Mysuru",
                "notes": "Updated test order"
            }
        )

    assert response.status_code == 200
    assert response.json["message"] == "Order updated successfully"
    assert response.json["order"]["ship_city"] == "Mysuru"


def test_update_order_not_found(client):
    with patch(
        "app.routes.order_routes.update_order",
        return_value=None
    ):
        response = client.put(
            "/orders/9999",
            json={"ship_city": "Mysuru"}
        )

    assert response.status_code == 404
    assert response.json["error"] == "Order not found"


def test_get_order_details(client):
    order_details = {
        "order_id": 10,
        "details": [
            {
                "detail_id": 1,
                "product_id": 7,
                "product_name": "Northwind Traders Dried Pears",
                "quantity": 10.0,
                "unit_price": 30.0,
                "discount": 0.0
            }
        ]
    }

    with patch(
        "app.routes.order_routes.get_order_details",
        return_value=order_details
    ):
        response = client.get("/orders/10/details")

    assert response.status_code == 200
    assert response.json["order_id"] == 10
    assert len(response.json["details"]) == 1
    assert response.json["details"][0]["product_id"] == 7


def test_order_details_not_found(client):
    with patch(
        "app.routes.order_routes.get_order_details",
        return_value=None
    ):
        response = client.get("/orders/9999/details")

    assert response.status_code == 404
    assert response.json["error"] == "Order not found"
