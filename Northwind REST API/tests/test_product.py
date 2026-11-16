
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


def sample_product():
    return SimpleNamespace(
        id=10,
        supplier_ids=None,
        product_code="TEST001",
        product_name="Test Laptop",
        description="Test product",
        standard_cost=45000,
        list_price=55000,
        reorder_level=5,
        target_level=20,
        quantity_per_unit="1 unit",
        discontinued=False,
        minimum_reorder_quantity=5,
        category="Electronics"
    )


def test_get_all_products(client):
    product = sample_product()

    with patch(
        "app.routes.product_routes.get_all_products",
        return_value=[product]
    ):
        response = client.get("/products")

    assert response.status_code == 200
    assert len(response.json["products"]) == 1
    assert response.json["products"][0]["id"] == 10


def test_get_product_by_id(client):
    product = sample_product()

    with patch(
        "app.routes.product_routes.get_product_by_id",
        return_value=product
    ):
        response = client.get("/products/10")

    assert response.status_code == 200
    assert response.json["product"]["id"] == 10
    assert response.json["product"]["product_name"] == "Test Laptop"


def test_product_not_found(client):
    with patch(
        "app.routes.product_routes.get_product_by_id",
        return_value=None
    ):
        response = client.get("/products/9999")

    assert response.status_code == 404
    assert response.json["error"] == "Product not found"


def test_create_product(client):
    product = sample_product()

    with patch(
        "app.routes.product_routes.create_product",
        return_value=product
    ):
        response = client.post(
            "/products",
            json={
                "product_code": "TEST001",
                "product_name": "Test Laptop",
                "description": "Test product",
                "standard_cost": 45000,
                "list_price": 55000,
                "category": "Electronics"
            }
        )

    assert response.status_code == 201
    assert response.json["message"] == "Product created successfully"
    assert response.json["product"]["id"] == 10



def test_update_product(client):
    product = sample_product()
    product.product_name = "Updated Laptop"
    product.list_price = 60000

    with patch(
        "app.routes.product_routes.update_product",
        return_value=product
    ):
        response = client.put(
            "/products/10",
            json={
                "product_name": "Updated Laptop",
                "list_price": 60000
            }
        )

    assert response.status_code == 200
    assert response.json["message"] == "Product updated successfully"
    assert response.json["product"]["product_name"] == "Updated Laptop"
    assert response.json["product"]["list_price"] == 60000



def test_update_product_not_found(client):
    with patch(
        "app.routes.product_routes.update_product",
        return_value=None
    ):
        response = client.put(
            "/products/9999",
            json={"product_name": "Updated Laptop"}
        )

    assert response.status_code == 404
    assert response.json["error"] == "Product not found"
