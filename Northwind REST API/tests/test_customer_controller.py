
from types import SimpleNamespace
from unittest.mock import patch

from app.controllers import customer_controller


def test_get_all_customers():
    customers = [
        SimpleNamespace(id=1, first_name="John"),
        SimpleNamespace(id=2, first_name="Jane")
    ]

    with patch.object(customer_controller, "Customer") as mock_customer:
        mock_customer.query.all.return_value = customers

        result = customer_controller.get_all_customers()

    assert len(result) == 2
    assert result[0].first_name == "John"


def test_get_customer_by_id():
    customer = SimpleNamespace(id=10, first_name="John")

    with patch(
        "app.controllers.customer_controller.db.session.get",
        return_value=customer
    ):
        result = customer_controller.get_customer_by_id(10)

    assert result.id == 10
    assert result.first_name == "John"


def test_create_customer():
    data = {
        "first_name": "John",
        "last_name": "Smith",
        "email_address": "john@example.com"
    }

    with patch(
        "app.controllers.customer_controller.db.session.add"
    ) as mock_add, patch(
        "app.controllers.customer_controller.commit_or_rollback"
    ) as mock_commit:

        result = customer_controller.create_customer(data)

    assert result.first_name == "John"
    assert result.last_name == "Smith"
    mock_add.assert_called_once_with(result)
    mock_commit.assert_called_once()


def test_update_customer():
    customer = SimpleNamespace(
        id=10,
        first_name="John",
        job_title="Developer"
    )

    with patch(
        "app.controllers.customer_controller.db.session.get",
        return_value=customer
    ), patch(
        "app.controllers.customer_controller.commit_or_rollback"
    ) as mock_commit:

        result = customer_controller.update_customer(
            10,
            {"job_title": "Senior Developer"}
        )

    assert result.job_title == "Senior Developer"
    mock_commit.assert_called_once()


def test_update_customer_not_found():
    with patch(
        "app.controllers.customer_controller.db.session.get",
        return_value=None
    ):
        result = customer_controller.update_customer(
            9999,
            {"first_name": "John"}
        )

    assert result is None


def test_delete_customer():
    customer = SimpleNamespace(id=10)

    with patch(
        "app.controllers.customer_controller.db.session.get",
        return_value=customer
    ), patch(
        "app.controllers.customer_controller.db.session.delete"
    ) as mock_delete, patch(
        "app.controllers.customer_controller.commit_or_rollback"
    ) as mock_commit:

        result = customer_controller.delete_customer(10)

    assert result is True
    mock_delete.assert_called_once_with(customer)
    mock_commit.assert_called_once()


def test_delete_customer_not_found():
    with patch(
        "app.controllers.customer_controller.db.session.get",
        return_value=None
    ):
        result = customer_controller.delete_customer(9999)

    assert result is False
