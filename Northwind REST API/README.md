# Northwind REST API

A REST API built using Python, Flask, Flask-SQLAlchemy, and MySQL to manage Northwind database records.

## Features

- Customer management: create, retrieve, update, and delete customers.
- Product management: create, retrieve, and update products.
- Order management: create, retrieve, and update orders.
- Retrieve order history for a customer.
- Retrieve details of a specific order.
- Input validation using Pydantic.
- Database operations using SQLAlchemy ORM.
- Unit and API route tests using pytest and mocking.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- MySQL
- PyMySQL
- Pydantic
- pytest
- pytest-mock

## Project Structure

```text
Northwind REST API/
│
├── app/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── validators/
│   ├── views/
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
│   └── test_order_controller.py
│
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## Prerequisites

- Python installed
- MySQL Server installed and running
- Existing Northwind database

The application connects to the existing Northwind database. It does not create or recreate database tables.

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

Replace the username and password with your own MySQL credentials.

## Running the Application

Start the Flask application:

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
| PUT | `/customers/<id>` | Update a customer |
| DELETE | `/customers/<id>` | Delete a customer |
| GET | `/customers/<id>/orders` | Retrieve customer order history |

### Product Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/products` | Retrieve all products |
| GET | `/products/<id>` | Retrieve a product |
| POST | `/products` | Create a product |
| PUT | `/products/<id>` | Update a product |

### Order Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/orders` | Retrieve all orders |
| GET | `/orders/<id>` | Retrieve an order |
| POST | `/orders` | Create an order |
| PUT | `/orders/<id>` | Update an order |
| GET | `/orders/<id>/details` | Retrieve order details |

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

The project currently has **38 passing tests** covering customer, product, and order routes and controller functions.

## Notes

- Database credentials are stored in `.env` and should not be committed to GitHub.
- The existing Northwind MySQL database is required.
- AWS deployment is not included in this project.