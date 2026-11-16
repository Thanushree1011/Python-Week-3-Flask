from app.models import Product
from app.extensions import db, commit_or_rollback

from app.validators.product_validator import (
    ProductCreate,
    ProductUpdate
)


def get_all_products():

    products = Product.query.all()

    return products


def get_product_by_id(product_id):

    product = db.session.get(Product, product_id)

    return product


def create_product(data):

    validated_data = ProductCreate(**data)

    product_data = validated_data.model_dump(
        exclude_unset=True
    )

    product = Product(**product_data)

    db.session.add(product)

    commit_or_rollback()

    return product


def update_product(product_id, data):

    product = db.session.get(Product, product_id)

    if not product:
        return None

    validated_data = ProductUpdate(**data)

    update_data = validated_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(product, key, value)

    commit_or_rollback()

    return product