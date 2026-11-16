# Northwind REST API

A REST API built with Python, Flask, Flask-SQLAlchemy and MySQL to manage records in the Northwind database.

## Features

- Customers: create, retrieve, update.
- Products: create, retrieve, update.
- Orders: create, retrieve, update, and view order details.
- Order history for a customer.
- Input validation with Pydantic (types, lengths, email format, non-negative amounts, date order).
- Database access through the SQLAlchemy ORM.
- Unit and route tests with pytest, with the database mocked.

## Technologies

Python, Flask, SQLAlchemy, MySQL, Pydantic, pytest

## Project Structure

```text
Northwind REST API/
│
├── app/
│   ├── controllers/   # business logic
│   ├── models/        # SQLAlchemy models
│   ├── routes/        # HTTP endpoints and JSON output
│   ├── validators/    # Pydantic schemas
│   ├── __init__.py
│   ├── config.py
│   └── extensions.py
│
├── tests/
│   ├── test_customer.py
│   ├── test_customer_controller.py
│   ├── test_product.py
│   ├── test_product_controller.py
│   ├── test_order.py
│   ├── test_order_controller.py
│   └── test_validators.py
│
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## Prerequisites

- Python 3.12 or newer
- MySQL Server installed and running
- An existing Northwind database

The application connects to the existing Northwind database. It does not create or recreate tables.

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Northwind-REST-API
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=northwind
MYSQL_PORT=3306
```

Replace the username and password with your own MySQL credentials. Do not commit this file or share it.

## Running the Application

```bash
python run.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

Check the database connection:

```text
http://127.0.0.1:5000/db-check
```

## API Endpoints

### Customer Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/customers` | Retrieve all customers |
| GET | `/customers/<id>` | Retrieve a customer |
| POST | `/customers` | Create a customer |
| PUT | `/customers/<id>` | Update a customer (partial updates allowed) |
| DELETE | `/customers/<id>` | Delete a customer (not possible if it has orders) |
| GET | `/customers/<id>/orders` | Retrieve customer order history |

### Product Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/products` | Retrieve all products |
| GET | `/products/<id>` | Retrieve a product |
| POST | `/products` | Create a product |
| PUT | `/products/<id>` | Update a product (partial updates allowed) |

### Order Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/orders` | Retrieve all orders |
| GET | `/orders/<id>` | Retrieve an order |
| POST | `/orders` | Create an order (`customer_id` is required) |
| PUT | `/orders/<id>` | Update an order |
| GET | `/orders/<id>/details` | Retrieve order details |

## Validation Rules

- Unknown fields are rejected.
- Customer: `email_address` must be a valid email address, and the request body cannot be empty.
- Product: `list_price` and `standard_cost` cannot be negative, and the request body cannot be empty.
- Order: `customer_id` is required and the customer must exist. `shipping_fee` and `taxes` cannot be negative. `shipped_date` cannot be before `order_date`.
- Text fields have maximum lengths that match the database columns.

## Response Codes

| Code | Meaning |
|---|---|
| 200 / 201 | Success / created |
| 400 | Invalid JSON or failed validation (details are in `errors`) |
| 404 | Record not found, or the customer does not exist when creating an order |
| 500 | Database error |

## Example Request

```powershell
curl.exe -X POST http://127.0.0.1:5000/orders -H "Content-Type: application/json" -d '{\"customer_id\":1,\"payment_type\":\"Check\"}'
```

## Running Tests

Run all tests:

```bash
python -m pytest -v
```

Run tests for a specific module:

```bash
python -m pytest tests/test_customer.py -v
```

## Test Results

The project currently has **45 passing tests** covering routes, controller functions and validators. The database is mocked, so no MySQL connection is needed to run the tests.

## Notes

- Database credentials are stored in `.env` and should not be committed to GitHub or shared.
- The existing Northwind MySQL database is required.
- Order lines cannot be created through the API. `GET /orders/<id>/details` reads existing ones.
- AWS deployment is not included in this project.