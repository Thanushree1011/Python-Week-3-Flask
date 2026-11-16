
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


def sample_customer():
    return SimpleNamespace(
        id=10,
        company="ABC Technologies",
        first_name="John",
        last_name="Smith",
        email_address="john@example.com",
        job_title="Developer",
        business_phone="9876543210",
        home_phone=None,
        mobile_phone=None,
        fax_number=None,
        address="123 Main Street",
        city="Bengaluru",
        state_province="Karnataka",
        zip_postal_code="560001",
        country_region="India",
        web_page=None,
        notes=None
    )


def test_get_all_customers(client):
    customer = sample_customer()

    with patch(
        "app.routes.customer_routes.get_all_customers",
        return_value=[customer]
    ):
        response = client.get("/customers")

    assert response.status_code == 200
    assert len(response.json["customers"]) == 1
    assert response.json["customers"][0]["id"] == 10


def test_get_customer_by_id(client):
    customer = sample_customer()

    with patch(
        "app.routes.customer_routes.get_customer_by_id",
        return_value=customer
    ):
        response = client.get("/customers/10")

    assert response.status_code == 200
    assert response.json["customer"]["id"] == 10
    assert response.json["customer"]["first_name"] == "John"


def test_customer_not_found(client):
    with patch(
        "app.routes.customer_routes.get_customer_by_id",
        return_value=None
    ):
        response = client.get("/customers/9999")

    assert response.status_code == 404
    assert response.json["error"] == "Customer not found"


def test_create_customer(client):
    customer = sample_customer()

    with patch(
        "app.routes.customer_routes.create_customer",
        return_value=customer
    ):
        response = client.post(
            "/customers",
            json={
                "first_name": "John",
                "last_name": "Smith",
                "email_address": "john@example.com",
                "company": "ABC Technologies"
            }
        )

    assert response.status_code == 201
    assert response.json["message"] == "Customer created successfully"
    assert response.json["customer"]["id"] == 10


def test_get_customer_order_history(client):
    order_history = {
        "customer_id": 10,
        "customer_name": "John Smith",
        "orders": [
            {
                "order_id": 31,
                "order_date": "2006-01-20T00:00:00",
                "payment_type": "Credit Card",
                "products": []
            }
        ]
    }

    with patch(
        "app.routes.customer_routes.get_customer_order_history",
        return_value=order_history
    ):
        response = client.get("/customers/10/orders")

    assert response.status_code == 200
    assert response.json["customer_id"] == 10
    assert len(response.json["orders"]) == 1
