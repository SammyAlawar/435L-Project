ecommerce_Alawar documentation
=============================

Overview
--------

This documentation provides an overview of the eCommerce application built by Sammy Alawar. The application consists of multiple services that work together to provide customer management, inventory management, sales tracking, and reviews management.

Services
--------

1. **Customer Management (customers_db.py)**:
   - Manages customer data, including registration, updates, and wallet operations.
   - Key APIs:
     - Register Customer
     - Update Customer
     - Delete Customer
     - Charge Wallet
     - Deduct Wallet

2. **Inventory Management (inventory_db.py)**:
   - Handles goods in the inventory, including adding, updating, and deducting stock.
   - Key APIs:
     - Add Goods
     - Update Goods
     - Deduct Goods
     - View All Goods
     - View Good Details (by name and category)

3. **Sales Management (sales_db.py)**:
   - Tracks sales and manages customer purchases.
   - Key APIs:
     - Display Available Goods
     - Get Goods Details
     - Make a Sale
     - Save Purchase History

4. **Reviews Management (reviews_db.py)**:
   - Allows customers to provide feedback on products.
   - Key APIs:
     - Submit Review
     - Update Review
     - Delete Review
     - Get Product Reviews
     - Get Customer Reviews
     - Moderate Reviews
     - Get Review Details
   
5. **Wishlist Management (wishlist_db.py)**:
   - Allows customers to manage their product wishlists.
   - Key APIs:
     - Create Wishlist Table
     - Add to Wishlist
     - Remove from Wishlist
     - Get Wishlist Items

Modules
-------

The following modules provide the core functionalities of the application:

.. toctree::
   :maxdepth: 2
   :caption: Contents

   customers_db
   inventory_db
   sales_db
   reviews_db
   wishlist_db

How to Contribute
-----------------

Contributions are welcome. Please follow the steps below to get started:
1. Fork the repository.
2. Clone your fork locally.
3. Make changes and add tests for your changes.
4. Commit and push your changes.
5. Open a pull request.

License
-------

This project is licensed under the MIT License. See the LICENSE file for details.

