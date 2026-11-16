
from types import SimpleNamespace
from unittest.mock import patch

from app.controllers import product_controller


def test_get_all_products():
    products = [
        SimpleNamespace(id=1, product_name="Chai"),
        SimpleNamespace(id=2, product_name="Chang")
    ]

    with patch.object(product_controller, "Product") as mock_product:
        mock_product.query.all.return_value = products

        result = product_controller.get_all_products()

    assert len(result) == 2
    assert result[0].product_name == "Chai"


def test_get_product_by_id():
    product = SimpleNamespace(id=10, product_name="Test Laptop")

    with patch(
        "app.controllers.product_controller.db.session.get",
        return_value=product
    ):
        result = product_controller.get_product_by_id(10)

    assert result.id == 10
    assert result.product_name == "Test Laptop"


def test_create_product():
    data = {
        "product_code": "TEST001",
        "product_name": "Test Laptop",
        "standard_cost": 45000,
        "list_price": 55000,
        "category": "Electronics"
    }

    with patch(
        "app.controllers.product_controller.db.session.add"
    ) as mock_add, patch(
        "app.controllers.product_controller.commit_or_rollback"
    ) as mock_commit:

        result = product_controller.create_product(data)

    assert result.product_name == "Test Laptop"
    assert result.list_price == 55000
    mock_add.assert_called_once_with(result)
    mock_commit.assert_called_once()


def test_update_product():
    product = SimpleNamespace(
        id=10,
        product_name="Test Laptop",
        list_price=55000
    )

    with patch(
        "app.controllers.product_controller.db.session.get",
        return_value=product
    ), patch(
        "app.controllers.product_controller.commit_or_rollback"
    ) as mock_commit:

        result = product_controller.update_product(
            10,
            {
                "product_name": "Updated Laptop",
                "list_price": 60000
            }
        )

    assert result.product_name == "Updated Laptop"
    assert result.list_price == 60000
    mock_commit.assert_called_once()


def test_update_product_not_found():
    with patch(
        "app.controllers.product_controller.db.session.get",
        return_value=None
    ):
        result = product_controller.update_product(
            9999,
            {"product_name": "Updated Laptop"}
        )

    assert result is None
