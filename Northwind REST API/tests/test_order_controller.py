
from types import SimpleNamespace
from unittest.mock import patch

from app.controllers import order_controller


def test_get_all_orders():
    orders = [
        SimpleNamespace(id=1),
        SimpleNamespace(id=2)
    ]

    with patch.object(order_controller, "Order") as mock_order:
        mock_order.query.all.return_value = orders

        result = order_controller.get_all_orders()

    assert len(result) == 2
    assert result[0].id == 1


def test_get_order_by_id():
    order = SimpleNamespace(id=10)

    with patch(
        "app.controllers.order_controller.db.session.get",
        return_value=order
    ):
        result = order_controller.get_order_by_id(10)

    assert result.id == 10


def test_create_order():
    data = {
        "customer_id": 4,
        "employee_id": 2,
        "ship_name": "Test Customer"
    }

    with patch(
        "app.controllers.order_controller.db.session.add"
    ) as mock_add, patch(
        "app.controllers.order_controller.commit_or_rollback"
    ) as mock_commit:

        result = order_controller.create_order(data)

    assert result.customer_id == 4
    assert result.employee_id == 2
    assert result.ship_name == "Test Customer"

    mock_add.assert_called_once_with(result)
    mock_commit.assert_called_once()


def test_update_order():
    order = SimpleNamespace(
        id=10,
        ship_city="Bengaluru",
        notes="Original notes"
    )

    with patch(
        "app.controllers.order_controller.db.session.get",
        return_value=order
    ), patch(
        "app.controllers.order_controller.commit_or_rollback"
    ) as mock_commit:

        result = order_controller.update_order(
            10,
            {
                "ship_city": "Mysuru",
                "notes": "Updated notes"
            }
        )

    assert result.ship_city == "Mysuru"
    assert result.notes == "Updated notes"
    mock_commit.assert_called_once()


def test_update_order_not_found():
    with patch(
        "app.controllers.order_controller.db.session.get",
        return_value=None
    ):
        result = order_controller.update_order(
            9999,
            {"ship_city": "Mysuru"}
        )

    assert result is None


def test_get_order_details():
    order = SimpleNamespace(id=10)

    detail = SimpleNamespace(
        id=1,
        product_id=7,
        quantity=10,
        unit_price=30,
        discount=0
    )

    product = SimpleNamespace(
        id=7,
        product_name="Dried Pears"
    )

    with patch.object(order_controller, "OrderDetail") as mock_detail, patch(
        "app.controllers.order_controller.db.session.get",
        side_effect=[order, product]
    ):
        mock_detail.query.filter_by.return_value.all.return_value = [detail]

        result = order_controller.get_order_details(10)

    assert result["order_id"] == 10
    assert len(result["details"]) == 1
    assert result["details"][0]["product_id"] == 7
    assert result["details"][0]["product_name"] == "Dried Pears"
    assert result["details"][0]["quantity"] == 10


def test_get_order_details_not_found():
    with patch(
        "app.controllers.order_controller.db.session.get",
        return_value=None
    ):
        result = order_controller.get_order_details(9999)

    assert result is None
