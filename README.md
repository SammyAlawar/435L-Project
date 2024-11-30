435L E-Commerce API Project

This project implements an E-Commerce API for managing customers, inventory, sales, reviews, and wishlists. Below is a breakdown of the key components and their respective purposes:

app.py: The main entry point for the application, hosting the API routes and integrating all services.
Customers/: Contains the logic and database models for managing customer data, including API endpoints for operations such as registration, updates, and wallet transactions.
Inventory/: Manages inventory-related functionality, including database models and APIs for adding, updating, and retrieving inventory items.
Sales/: Handles sales processing, including APIs for managing transactions and updating stock and customer purchase histories.
Reviews/: Includes database models and API routes for managing product reviews, such as submitting, updating, and moderating reviews.
Wishlist/: Implements functionality for managing wishlists, allowing customers to add, remove, and view saved products.
docs/: Contains API documentation and additional resources, including Sphinx generated files.
tests/: Includes unit and integration tests for each service to ensure robustness and correctness.
database.db: The SQLite database file used to persist application data.
Docker/: Contains Docker-related files, such as the Dockerfile and docker-compose.yml, for containerizing and orchestrating the application.
requirements.txt: Lists the Python dependencies required to run the application.
