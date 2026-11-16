from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
import json
from app.controllers.product_controller import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product
)


product_bp = Blueprint("product", __name__)


def product_to_dict(product):

    return {
        "id": product.id,
        "supplier_ids": product.supplier_ids,
        "product_code": product.product_code,
        "product_name": product.product_name,
        "description": product.description,
        "standard_cost": (
            float(product.standard_cost)
            if product.standard_cost is not None
            else None
        ),
        "list_price": float(product.list_price),
        "reorder_level": product.reorder_level,
        "target_level": product.target_level,
        "quantity_per_unit": product.quantity_per_unit,
        "discontinued": product.discontinued,
        "minimum_reorder_quantity": product.minimum_reorder_quantity,
        "category": product.category
    }


def handle_error(error):
    return jsonify({"errors": json.loads(error.json(include_url=False))}), 400


@product_bp.route("/products", methods=["GET"])
def list_products():

    try:
        products = get_all_products()

        return jsonify({
            "products": [
                product_to_dict(product)
                for product in products
            ]
        }), 200

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500


@product_bp.route("/products/<int:product_id>", methods=["GET"])
def retrieve_product(product_id):

    try:
        product = get_product_by_id(product_id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        return jsonify({
            "product": product_to_dict(product)
        }), 200

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500


@product_bp.route("/products", methods=["POST"])
def add_product():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    try:
        product = create_product(data)

        return jsonify({
            "message": "Product created successfully",
            "product": product_to_dict(product)
        }), 201

    except ValidationError as error:
        return handle_error(error)

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500


@product_bp.route("/products/<int:product_id>", methods=["PUT"])
def edit_product(product_id):

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    try:
        product = update_product(product_id, data)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        return jsonify({
            "message": "Product updated successfully",
            "product": product_to_dict(product)
        }), 200

    except ValidationError as error:
        return handle_error(error)

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500