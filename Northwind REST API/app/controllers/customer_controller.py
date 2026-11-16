from app.models import Customer, Order, OrderDetail, Product
from app.extensions import db, commit_or_rollback
from app.validators.customer_validator import (
    CustomerCreate,
    CustomerUpdate
)
from sqlalchemy.orm import selectinload


def get_all_customers():

    customers = Customer.query.all()

    return customers


def get_customer_by_id(customer_id):

    customer = db.session.get(Customer, customer_id)

    return customer


def create_customer(data):

    validated_data = CustomerCreate(**data)

    customer_data = validated_data.model_dump(
        exclude_unset=True
    )

    customer = Customer(**customer_data)

    db.session.add(customer)

    commit_or_rollback()

    return customer


def update_customer(customer_id, data):

    customer = db.session.get(Customer, customer_id)

    if not customer:
        return None

    validated_data = CustomerUpdate(**data)

    update_data = validated_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(customer, key, value)

    commit_or_rollback()

    return customer


def delete_customer(customer_id):

    customer = db.session.get(Customer, customer_id)

    if not customer:
        return False

    db.session.delete(customer)

    commit_or_rollback()

    return True

def get_customer_order_history(customer_id):
    # Eagerly load orders -> order_details -> product in optimized queries
    customer = db.session.get(Customer, customer_id, options=[
        selectinload(Customer.orders).selectinload(Order.order_details).selectinload(OrderDetail.product)
    ])

    if not customer:
        return None

    result = []
    for order in customer.orders:
        products = []
        for detail in order.order_details:
            product = detail.product  # Already loaded via eager loading!
            if product:
                products.append({
                    "product_id": product.id,
                    "product_name": product.product_name,
                    "quantity": float(detail.quantity) if detail.quantity is not None else None,
                    "unit_price": float(detail.unit_price) if detail.unit_price is not None else None,
                    "discount": detail.discount
                })

        result.append({
            "order_id": order.id,
            "order_date": order.order_date.isoformat() if order.order_date else None,
            "payment_type": order.payment_type,
            "products": products
        })

    return {
        "customer_id": customer.id,
        "customer_name": f"{customer.first_name or ''} {customer.last_name or ''}".strip(),
        "orders": result
    }