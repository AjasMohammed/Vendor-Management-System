# Vendor Management System API

This project implements a Vendor Management System API using Django and Django REST Framework.

## Description

The Vendor Management System API provides endpoints to manage vendors, purchase orders, vendor performance, and authentication functionalities.

## Features

- **Vendor Management:**
  - Create, retrieve, update, and delete vendors.
  - View vendor performance metrics.

- **Purchase Order Management:**
  - Initiate, retrieve, update, and delete purchase orders.
  - Acknowledge purchase orders.

- **Authentication:**
  - User registration (Sign Up).
  - User login (Log In) and logout (Log Out).

## Project Structure

The project structure is organized as follows:

- **API (api/):**
  - Contains the implementation of API endpoints for vendor and purchase order management.

- **Authentication (auth/):**
  - Manages user registration, login, and logout.

- **Endpoints:**
  - `/api/vendor/`: Vendor management endpoints.
  - `/api/purchase_orders/`: Purchase order management endpoints.
  - `/auth/signup/`: User registration endpoint.
  - `/auth/login/`: User login endpoint.
  - `/auth/logout/`: User logout endpoint.

## Installation

To set up and run the project locally:

1. Clone this repository.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Set up the database using Django migrations: `python manage.py makemigrations` and `python manage.py migrate`.
4. Run the development server: `python manage.py runserver`.

## Usage

- Access the provided endpoints using appropriate HTTP requests (GET, POST, PUT, DELETE) with required parameters and authentication tokens.
- Utilize the provided authentication endpoints to register, login, and logout users.
- Ensure proper permissions and authentication for accessing restricted endpoints.

## Testing

The project includes a suite of tests using `pytest` to ensure the functionality and reliability of the implemented endpoints. Run tests using the command: `pytest`.

## Documentation

- The API is documented using Swagger.
- Access API documentation:
  - Swagger UI: `/api/docs/`

## Contributing

Contributions and suggestions are welcome! Fork this repository, make changes, and submit a pull request.

