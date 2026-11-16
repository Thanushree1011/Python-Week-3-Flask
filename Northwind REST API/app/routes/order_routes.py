
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.controllers.order_controller import (
    get_all_orders,
    get_order_by_id,
    create_order,
    update_order,
    get_order_details
)

order_bp = Blueprint("order", __name__)


def order_to_dict(order):
    return {
        "id": order.id,
        "employee_id": order.employee_id,
        "customer_id": order.customer_id,
        "order_date": order.order_date.isoformat() if order.order_date else None,
        "shipped_date": order.shipped_date.isoformat() if order.shipped_date else None,
        "shipper_id": order.shipper_id,
        "ship_name": order.ship_name,
        "ship_address": order.ship_address,
        "ship_city": order.ship_city,
        "ship_state_province": order.ship_state_province,
        "ship_zip_postal_code": order.ship_zip_postal_code,
        "ship_country_region": order.ship_country_region,
        "shipping_fee": float(order.shipping_fee) if order.shipping_fee is not None else None,
        "taxes": float(order.taxes) if order.taxes is not None else None,
        "payment_type": order.payment_type,
        "paid_date": order.paid_date.isoformat() if order.paid_date else None,
        "notes": order.notes,
        "tax_rate": order.tax_rate,
        "tax_status_id": order.tax_status_id,
        "status_id": order.status_id
    }


def handle_error(error):
    return jsonify({
        "errors": error.errors(include_url=False)
    }), 400


@order_bp.route("/orders", methods=["GET"])
def list_orders():
    try:
        orders = get_all_orders()

        return jsonify({
            "orders": [order_to_dict(order) for order in orders]
        }), 200

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500


@order_bp.route("/orders/<int:order_id>", methods=["GET"])
def retrieve_order(order_id):
    try:
        order = get_order_by_id(order_id)

        if not order:
            return jsonify({"error": "Order not found"}), 404

        return jsonify({
            "order": order_to_dict(order)
        }), 200

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500


@order_bp.route("/orders", methods=["POST"])
def add_order():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object"
        }), 400

    try:
        order = create_order(data)

        return jsonify({
            "message": "Order created successfully",
            "order": order_to_dict(order)
        }), 201

    except ValidationError as error:
        return handle_error(error)

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500


@order_bp.route("/orders/<int:order_id>", methods=["PUT"])
def edit_order(order_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object"
        }), 400

    try:
        order = update_order(order_id, data)

        if not order:
            return jsonify({"error": "Order not found"}), 404

        return jsonify({
            "message": "Order updated successfully",
            "order": order_to_dict(order)
        }), 200

    except ValidationError as error:
        return handle_error(error)

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500

    
@order_bp.route("/orders/<int:order_id>/details", methods=["GET"])
def retrieve_order_details(order_id):
    try:
        result = get_order_details(order_id)

        if result is None:
            return jsonify({"error": "Order not found"}), 404

        return jsonify(result), 200

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500

