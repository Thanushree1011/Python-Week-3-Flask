

from app.extensions import db, commit_or_rollback
from app.validators.order_validator import OrderCreate, OrderUpdate
from app.models import Order, OrderDetail, Product

def get_all_orders():
    return Order.query.all()


def get_order_by_id(order_id):
    return db.session.get(Order, order_id)


def create_order(data):
    validated_data = OrderCreate(**data)

    order_data = validated_data.model_dump(exclude_unset=True)

    order = Order(**order_data)

    db.session.add(order)
    commit_or_rollback()

    return order


def update_order(order_id, data):
    order = db.session.get(Order, order_id)

    if not order:
        return None

    validated_data = OrderUpdate(**data)

    update_data = validated_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(order, key, value)

    commit_or_rollback()

    return order


def get_order_details(order_id):
    order = db.session.get(Order, order_id)

    if not order:
        return None

    details = OrderDetail.query.filter_by(order_id=order_id).all()

    result = []

    for detail in details:
        product = db.session.get(Product, detail.product_id)

        result.append({
            "detail_id": detail.id,
            "product_id": detail.product_id,
            "product_name": product.product_name if product else None,
            "quantity": float(detail.quantity) if detail.quantity is not None else None,
            "unit_price": float(detail.unit_price) if detail.unit_price is not None else None,
            "discount": detail.discount
        })

    return {
        "order_id": order.id,
        "details": result
    }

