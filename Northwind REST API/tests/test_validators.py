import pytest
from pydantic import ValidationError

from app.validators.customer_validator import CustomerCreate
from app.validators.order_validator import OrderCreate
from app.validators.product_validator import ProductCreate


def test_customer_rejects_bad_email():
    with pytest.raises(ValidationError):
        CustomerCreate(email_address="not-an-email")


def test_customer_rejects_empty_body():
    with pytest.raises(ValidationError):
        CustomerCreate()


def test_product_rejects_negative_price():
    with pytest.raises(ValidationError):
        ProductCreate(list_price="-1")


def test_order_requires_customer_id():
    with pytest.raises(ValidationError):
        OrderCreate()


def test_order_rejects_shipped_before_ordered():
    with pytest.raises(ValidationError):
        OrderCreate(customer_id=1, order_date="2026-02-01", shipped_date="2026-01-01")


def test_order_valid():
    assert OrderCreate(customer_id=1, shipping_fee="5").customer_id == 1