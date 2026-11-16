from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.controllers.customer_controller import (
    get_all_customers,
    get_customer_by_id,
    create_customer,
    update_customer,
    delete_customer,
    get_customer_order_history
)


customer_bp = Blueprint("customer", __name__)


def customer_to_dict(customer):

    return {
        "id": customer.id,
        "company": customer.company,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email_address": customer.email_address,
        "job_title": customer.job_title,
        "business_phone": customer.business_phone,
        "home_phone": customer.home_phone,
        "mobile_phone": customer.mobile_phone,
        "fax_number": customer.fax_number,
        "address": customer.address,
        "city": customer.city,
        "state_province": customer.state_province,
        "zip_postal_code": customer.zip_postal_code,
        "country_region": customer.country_region,
        "web_page": customer.web_page,
        "notes": customer.notes
    }


def handle_error(error):

    return jsonify({
        "errors": error.errors(include_url=False)
    }), 400


@customer_bp.route("/customers", methods=["GET"])
def list_customers():

    try:
        customers = get_all_customers()

        return jsonify({
            "customers": [
                customer_to_dict(customer)
                for customer in customers
            ]
        }), 200

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500


@customer_bp.route("/customers/<int:customer_id>", methods=["GET"])
def retrieve_customer(customer_id):

    try:
        customer = get_customer_by_id(customer_id)

        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        return jsonify({
            "customer": customer_to_dict(customer)
        }), 200

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500


@customer_bp.route("/customers", methods=["POST"])
def add_customer():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    try:
        customer = create_customer(data)

        return jsonify({
            "message": "Customer created successfully",
            "customer": customer_to_dict(customer)
        }), 201

    except ValidationError as error:
        return handle_error(error)

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500


@customer_bp.route("/customers/<int:customer_id>", methods=["PUT"])
def edit_customer(customer_id):

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    try:
        customer = update_customer(customer_id, data)

        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        return jsonify({
            "message": "Customer updated successfully",
            "customer": customer_to_dict(customer)
        }), 200

    except ValidationError as error:
        return handle_error(error)

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500


@customer_bp.route("/customers/<int:customer_id>", methods=["DELETE"])
def remove_customer(customer_id):

    try:
        deleted = delete_customer(customer_id)

        if not deleted:
            return jsonify({"error": "Customer not found"}), 404

        return jsonify({
            "message": "Customer deleted successfully"
        }), 200

    except SQLAlchemyError:
        return jsonify({
            "error": "Could not delete customer. Check whether it has related orders."
        }), 500


@customer_bp.route("/customers/<int:customer_id>/orders", methods=["GET"])
def customer_orders(customer_id):

    try:
        history = get_customer_order_history(customer_id)

        if not history:
            return jsonify({"error": "Customer not found"}), 404

        return jsonify(history), 200

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500