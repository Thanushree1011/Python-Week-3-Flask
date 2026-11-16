from flask import Flask, jsonify
from pydantic import ValidationError
from sqlalchemy import text

from app.config import Config
from app.extensions import db
from app.models import Customer, Product, Order, OrderDetail
from app.routes.customer_routes import customer_bp
from app.routes.product_routes import product_bp
from app.routes.order_routes import order_bp

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(customer_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    
    @app.route("/")
    def home():
        return jsonify({
            "message": "Northwind REST API is running!"
        })

    @app.route("/db-check")
    def db_check():

        try:
            result = db.session.execute(
                text("SELECT DATABASE()")
            ).scalar()

            return jsonify({
                "message": "Database connected successfully!",
                "database": result
            })

        except Exception:
            return jsonify({
                "error": "Database connection failed"
            }), 500

    return app