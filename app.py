from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import generate_password_hash
from Customers.customers_db import (
    create_customers_table,
    register_customer,
    delete_customer,
    update_customer,
    get_all_customers,
    get_customer_by_username,
    charge_customer_wallet,
    deduct_customer_wallet,
    get_customer_wallet
)
import logging
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests
app.config['TESTING'] = True  # Enable testing mode for easier debugging
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Ensures cookies are only sent via HTTP(S)
app.config['SESSION_COOKIE_SECURE'] = False  # Change to True if using HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
@app.route('/')
def home():
    """
    Default route that returns a welcome message for authenticated users.

    Returns:
        Response: JSON welcome message.
    """
    return jsonify({"message": "Welcome to the Customer Management API!"})

create_customers_table()
@app.route('/customers/get_all_customers', methods=['GET'])
def api_get_all_customers():
    """
    Retrieves all customers from the database.

    Returns:
        Response: JSON list of all customers.
    """
    customers = get_all_customers()
    return jsonify(customers)

@app.route('/customers/get_customer/<string:username>', methods=['GET'])
def api_get_customer_by_username(username):
    """
    Retrieves a specific customer by their username.

    Args:
        username (str): The username of the customer.

    Returns:
        Response: JSON object of the customer or error message.
    """
    customer = get_customer_by_username(username)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer)

@app.route('/customers/register', methods=['POST'])
def api_register_customer():
    """
    Registers a new customer in the database.

    Request JSON:
    - full_name (str)
    - username (str)
    - password (str)
    - age (int)
    - address (str)
    - gender (str)
    - marital_status (str)
    - wallet (float)

    Returns:
        Response: JSON object of the registered customer or error message.
    """
    customer = request.get_json()
    required_fields = ['full_name', 'username', 'password', 'age', 'address', 'gender', 'marital_status', 'wallet']
    missing_fields = [field for field in required_fields if field not in customer]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400
    if not isinstance(customer.get('age'), int) or customer['age'] <= 0:
        return jsonify({"error": "Invalid age. Must be a positive integer."}), 400
    if not isinstance(customer.get('wallet'), (int, float)) or customer['wallet'] < 0:
        return jsonify({"error": "Invalid wallet value. Must be a non-negative number."}), 400
    existing_customer = get_customer_by_username(customer.get('username'))
    if existing_customer:
        return jsonify({"error": "Customer with this username already exists"}), 409
    customer['password'] = bcrypt.generate_password_hash(customer['password']).decode('utf-8')
    registered_customer = register_customer(customer)
    if not registered_customer:
        return jsonify({"error": "Could not register customer"}), 500
    return jsonify(registered_customer), 201

@app.route('/customers/delete/<string:username>', methods=['DELETE'])
def api_delete_customer(username):
    """
    Deletes a customer from the database by their username.

    Args:
        username (str): The username of the customer.

    Returns:
        Response: JSON message indicating success or failure.
    """
    success = delete_customer(username)
    if not success:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify({"message": f"Customer '{username}' deleted successfully."})

@app.route('/customers/update/<string:username>', methods=['PUT'])
def api_update_customer(username):
    """
    Updates a customer's details.

    Args:
        username (str): The username of the customer.

    Request JSON:
    - Fields to update.

    Returns:
        Response: JSON message indicating success or failure.
    """
    updates = request.get_json()
    if not updates:
        return jsonify({"error": "Invalid input"}), 400
    success = update_customer(username, updates)
    if not success:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify({"message": f"Customer '{username}' updated successfully."})

@app.route('/customers/get_customer/<string:username>/charge/<string:amount>', methods=['POST'])
def api_charge_wallet(username, amount):
    """
    Charges a specified amount to a customer's wallet.

    Args:
        username (str): The username of the customer.
        amount (str): The amount to charge.

    Returns:
        Response: JSON message indicating success or failure.
    """
    try:
        amount = int(amount)
    except ValueError:
        return jsonify({"error": "Amount must be a valid integer."}), 400
    if amount <= 0:
        return jsonify({"error": "Amount must be greater than zero"}), 400
    customer = get_customer_by_username(username)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    success = charge_customer_wallet(username, amount)
    wallet = get_customer_wallet(username)
    if not success:
        return jsonify({"error": "Could not charge wallet"}), 500
    return jsonify({"message": f"Charged ${amount} to '{username}' wallet successfully. Total Balance: ${wallet}", "wallet": wallet}), 200

@app.route('/customers/get_customer/<string:username>/deduct/<int:amount>', methods=['POST'])
def api_deduct_wallet(username, amount):
    """
    Deducts a specified amount from a customer's wallet.

    Args:
        username (str): The username of the customer.
        amount (int): The amount to deduct.

    Returns:
        Response: JSON message indicating success or failure.
    """
    if amount <= 0:
        return jsonify({"error": "Amount must be greater than zero"}), 400
    success = deduct_customer_wallet(username, amount)
    wallet = get_customer_wallet(username)
    if not success:
        return jsonify({"error": "Customer not found, insufficient balance, or could not deduct wallet"}), 400
    return jsonify({"message": f"Deducted ${amount} from '{username}' wallet successfully. Total Balance: ${wallet}", "wallet": wallet})


'''APIs for Inventory'''

from Inventory.inventory_db import (
    create_inventory_table,
    add_goods,
    deduct_goods,
    update_goods,
    get_all_goods,
    get_good_by_name_and_category
)

# Ensure the Inventory table exists
create_inventory_table()

@app.route('/inventory/add_goods', methods=['POST'])
def api_add_goods():
    """
    API to add new goods to the inventory.

    Request JSON:
    - name (str): Name of the product.
    - category (str): Category of the product.
    - price_per_item (float): Price per item of the product.
    - description (str): Description of the product.
    - stock_count (int): Quantity of the product in stock.

    Returns:
        Response: JSON object with details of the added goods or an error message.
    """
    required_fields = ['name', 'category', 'price_per_item', 'description', 'stock_count']
    goods = request.get_json()

    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in goods]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Validate 'price_per_item' and 'stock_count'
    if not isinstance(goods.get('stock_count'), int) or goods['stock_count'] < 0:
        return jsonify({"error": "Invalid stock_count. Must be a non-negative integer."}), 400
    if not isinstance(goods.get('price_per_item'), (int, float)) or goods['price_per_item'] <= 0:
        return jsonify({"error": "Invalid price_per_item. Must be a positive number."}), 400

    added_goods = add_goods(goods)
    if not added_goods:
        return jsonify({"error": "Could not register goods"}), 500

    return jsonify(added_goods), 201

@app.route('/inventory/deduct_goods/<string:name>/<string:category>/<int:quantity>', methods=['POST'])
def api_deduct_goods(name, category, quantity):
    """
    API to deduct a quantity from an item's stock in the inventory.

    Args:
        name (str): Name of the product.
        category (str): Category of the product.
        quantity (int): Quantity to deduct from stock.

    Returns:
        Response: JSON object with success message or error details.
    """
    # Validate input
    if quantity <= 0:
        return jsonify({"error": "Quantity must be a positive integer."}), 400

    # Call the deduct_goods function
    result = deduct_goods(name, category, quantity)

    # Handle the result
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 200

@app.route('/inventory/update_goods/update', methods=['PUT'])
def api_update_goods():
    """
    API to update fields of an item in the inventory.

    Request JSON:
    - name (str): Name of the product.
    - category (str): Category of the product.
    - updates (dict): Dictionary containing the fields to update.

    Returns:
        Response: JSON message indicating success or failure.
    """
    data = request.get_json()

    # Validate input
    name = data.get('name')
    category = data.get('category')
    updates = data.get('updates')

    if not name or not category or not updates:
        return jsonify({"error": "Invalid input. Name, category, and updates are required."}), 400

    # Check if the item exists in the inventory
    existing_good = get_good_by_name_and_category(name, category)
    if "error" in existing_good:
        return jsonify({"error": f"Item '{name}' in category '{category}' not found."}), 404

    # Call the update_goods function
    result = update_goods(name, category, updates)

    # Handle the result
    if "error" in result:
        return jsonify(result), 400

    return jsonify({"message": "Goods updated successfully", "result": result}), 200

@app.route('/inventory/get_all_goods', methods=['GET'])
def api_get_all_goods():
    """
    API to retrieve all goods from the inventory.

    Returns:
        Response: JSON list of all goods.
    """
    goods = get_all_goods()
    return jsonify(goods), 200

@app.route('/inventory/get_goods/<string:name>/<string:category>', methods=['GET'])

def api_get_good_by_name_and_category(name, category):
    """
    API to retrieve a specific good by name and category.

    Args:
        name (str): Name of the product.
        category (str): Category of the product.

    Returns:
        Response: JSON object of the good or error message.
    """
    good = get_good_by_name_and_category(name, category)
    if "error" in good:
        return jsonify(good), 404
    return jsonify(good), 200


"""        Sales        """
from Sales.sales_db import (
    create_purchase_history_table,
    save_purchase_history
)

# Ensure the Sales table exists
create_purchase_history_table()

@app.route('/sales/purchase', methods=['POST'])

def api_make_sale():
    """
    API to process a sale by deducting customer funds and inventory stock.

    Request JSON:
    - username (str): Username of the customer making the purchase.
    - good_name (str): Name of the product being purchased.
    - category (str): Category of the product.
    - quantity (int): Quantity of the product being purchased.

    Returns:
        Response: JSON object indicating success or error details.
    """
    data = request.get_json()

    # Extract input parameters
    username = data.get('username')
    good_name = data.get('good_name')
    category = data.get('category')
    quantity = data.get('quantity')

    # Validate input
    if not username or not good_name or not category or not quantity:
        return jsonify({"error": "Invalid input. All fields are required."}), 400

    # Step 1: Check if the customer has enough money
    customer = get_customer_by_username(username)
    if 'error' in customer:
        return jsonify({"error": "Customer not found."}), 404

    good = get_good_by_name_and_category(good_name, category)
    if 'error' in good:
        return jsonify({"error": "Good not found."}), 404

    # Check if the customer has enough balance to buy the goods
    total_cost = good['price_per_item'] * quantity
    wallet = get_customer_wallet(username)
    if wallet < total_cost:
        return jsonify({"error": "Insufficient funds."}), 400

    # Step 2: Check if the good is available in stock
    if good['stock_count'] < quantity:
        return jsonify({"error": "Insufficient stock."}), 400

    # Step 3: Process the transaction (deduct wallet and reduce stock)
    success_wallet_deduction = deduct_customer_wallet(username, total_cost)
    wallet = get_customer_wallet(username)
    if not success_wallet_deduction:
        return jsonify({"error": "Error deducting from wallet."}), 500
    
    # Update the inventory by deducting the goods
    result = deduct_goods(good_name, category, quantity)
    if "error" in result:
        return jsonify(result), 400

    # Step 4: Save the purchase to the history
    save_purchase_history(username, good_name, quantity, total_cost)

    return jsonify({"message": f"Purchased {quantity} {good_name}(s) for ${total_cost}. Total Balance: ${wallet}"}), 200


"""        Reviews        """

from Reviews.reviews_db import (
    create_reviews_table,
    submit_review,
    update_review,
    delete_review,
    get_product_reviews,
    get_customer_reviews,
    moderate_review,
    get_review_details
)
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

# Configure secret key for session management
app.config['SECRET_KEY'] = 'a4d7f5e41f72d5c8b1c5f34a8cb7311c67a23d4e5f6b7c8d9a0e1f2a3b4c5d6e'

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect users to 'login' if unauthorized

# Initialize Bcrypt with your Flask app
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    """
    This function is called to load a user by their ID during a session.

    Args:
        user_id (str): The unique ID of the user.

    Returns:
        User: The User object if the user exists, otherwise None.
    """
    user = get_customer_by_username(user_id)  # Fetch user from database
    if user:
        return User(user['id'], user['username'], user['password'])
    return None


class User(UserMixin):
    """
    Represents a user for Flask-Login.

    Attributes:
        id (str): The unique ID of the user.
        username (str): The username of the user.
        password (str): The hashed password of the user.
    """
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


@app.route('/login', methods=['POST'])
def login():
    """
    Logs in a user by validating their username and password.

    Request JSON:
    - username (str): The username of the user.
    - password (str): The plaintext password of the user.

    Logic:
    - Fetch the user from the database using the provided username.
    - Compare the provided password with the stored hashed password.
    - If valid, log the user in and return a success message.
    - If invalid, return an error message.

    Returns:
        Response: A JSON response with a success or error message.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Fetch the user from the database
    user = get_customer_by_username(username)

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    # Validate the password
    if bcrypt.check_password_hash(user['password'], password):
        login_user(User(user['id'], user['username'], user['password']))
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Invalid username or password"}), 401

@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({"message": f"Hello, {current_user.username}!"}), 200


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Logs out the currently logged-in user.

    Logic:
    - Ends the user session using Flask-Login's `logout_user` function.
    - Returns a success message indicating the user has been logged out.

    Returns:
        Response: A JSON response confirming the logout.
    """
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

from flask_login import current_user, login_required

@app.route('/reviews/submit', methods=['POST'])
@login_required
def api_submit_review():
    """
    API to submit a review for a product. Only authenticated users can submit reviews.

    Request JSON:
    - product_name (str): Name of the product being reviewed.
    - username (str): Username of the customer submitting the review.
    - rating (int): Rating for the product (1-5).
    - comment (str): Optional comment for the review.

    Returns:
        Response: JSON object with success message or error details.
    """
    data = request.get_json()

    # Validate input
    product_name = data.get('product_name')
    rating = data.get('rating')
    comment = data.get('comment')

    if not product_name or not rating or not (1 <= rating <= 5):
        return jsonify({"error": "Invalid input. Product name and a valid rating (1-5) are required."}), 400

    # Ensure the review is being submitted by the authenticated user
    username = current_user.username

    # Submit the review
    submit_review(product_name, username, rating, comment)

    return jsonify({"message": f"Successfully submitted {rating} star review.", "rating": rating}), 201


@app.route('/reviews/update/<int:review_id>', methods=['PUT'])
@login_required
def api_update_review(review_id):
    """
    API to update an existing review. Only the review owner can update the review.

    Request JSON:
    - rating (int): New rating for the product (1-5).
    - comment (str): Updated comment for the review.

    Args:
        review_id (int): ID of the review to update.

    Returns:
        Response: JSON object with success message or error details.
    """
    data = request.get_json()

    rating = data.get('rating')
    comment = data.get('comment')

    if not (1 <= rating <= 5):
        return jsonify({"error": "Rating must be between 1 and 5."}), 400

    # Check if the review belongs to the current user
    review = get_review_details(review_id)
    if not review:
        return jsonify({"error": "Review not found."}), 404
    if review['username'] != current_user.username:
        return jsonify({"error": "Unauthorized action. You can only update your own reviews."}), 403

    # Call the function to update the review
    update_review(review_id, rating, comment)
    return jsonify({"message": "Review updated successfully."}), 200


@app.route('/reviews/delete/<int:review_id>', methods=['DELETE'])
@login_required
def api_delete_review(review_id):
    """
    API to delete an existing review. Only the review owner can delete the review.

    Args:
        review_id (int): ID of the review to delete.

    Returns:
        Response: JSON object with success message or error details.
    """
    # Check if the review belongs to the current user
    review = get_review_details(review_id)
    if not review:
        return jsonify({"error": "Review not found."}), 404
    if review['username'] != current_user.username:
        return jsonify({"error": "Unauthorized action. You can only delete your own reviews."}), 403

    # Call the function to delete the review
    delete_review(review_id)
    return jsonify({"message": "Review deleted successfully."}), 200


@app.route('/reviews/product/<string:product_name>', methods=['GET'])

def api_get_product_reviews(product_name):
    """
    API to retrieve all reviews for a specific product.

    Args:
        product_name (str): Name of the product.

    Returns:
        Response: JSON object with list of reviews or a message if no reviews are found.
    """
    reviews = get_product_reviews(product_name)
    if not reviews:
        return jsonify({"message": "No reviews found for this product."}), 404
    return jsonify(reviews), 200

@app.route('/reviews/customer/<string:username>', methods=['GET'])

def api_get_customer_reviews(username):
    """
    API to retrieve all reviews submitted by a specific customer.

    Args:
        username (str): Username of the customer.

    Returns:
        Response: JSON object with list of reviews or a message if no reviews are found.
    """
    reviews = get_customer_reviews(username)
    if not reviews:
        return jsonify({"message": "No reviews found for this customer."}), 404
    return jsonify(reviews), 200

@app.route('/reviews/moderate/<int:review_id>', methods=['PATCH'])

def api_moderate_review(review_id):
    """
    API to moderate a review by toggling its moderation status.

    Request JSON:
    - moderated (bool): New moderation status for the review.

    Args:
        review_id (int): ID of the review to moderate.

    Returns:
        Response: JSON object with success message or error details.
    """
    data = request.get_json()
    moderated = data.get('moderated')

    if moderated not in [True, False]:
        return jsonify({"error": "Invalid moderation status."}), 400

    # Call the function to moderate the review
    moderate_review(review_id, moderated)
    return jsonify({"message": "Review moderation updated successfully."}), 200

@app.route('/reviews/details/<int:review_id>', methods=['GET'])

def api_get_review_details(review_id):
    """
    API to retrieve details of a specific review.

    Args:
        review_id (int): ID of the review.

    Returns:
        Response: JSON object with review details or error message if not found.
    """
    review = get_review_details(review_id)
    if not review:  # If review doesn't exist
        return jsonify({"error": "Review not found."}), 404
    return jsonify(review), 200

"""        Wishlist        """

from Wishlist.wishlist_db import (
    create_wishlist_table,
    add_to_wishlist,
    remove_from_wishlist,
    get_wishlist
)

# Ensure the Wishlist table exists
create_wishlist_table()

@app.route('/wishlist/add', methods=['POST'])

def api_add_to_wishlist():
    """
    API to add a product to the user's wishlist.

    Request JSON:
    - product_id (int): ID of the product to add.

    Returns:
        Response: JSON object with success message or error details.
    """
    data = request.get_json()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    add_to_wishlist(current_user.id, product_id)
    return jsonify({"message": "Product added to wishlist successfully."}), 201

@app.route('/wishlist/remove', methods=['POST'])

def api_remove_from_wishlist():
    """
    API to remove a product from the user's wishlist.

    Request JSON:
    - product_id (int): ID of the product to remove.

    Returns:
        Response: JSON object with success message or error details.
    """
    data = request.get_json()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    remove_from_wishlist(current_user.id, product_id)
    return jsonify({"message": "Product removed from wishlist successfully."}), 200

@app.route('/wishlist', methods=['GET'])

def api_get_wishlist():
    """
    API to fetch all products in the user's wishlist.

    Returns:
        Response: JSON object with the wishlist items or a message if the wishlist is empty.
    """
    wishlist = get_wishlist(current_user.id)
    if not wishlist:
        return jsonify({"message": "Wishlist is empty."}), 200

    return jsonify({"wishlist": wishlist}), 200

# Run the application
if __name__ == "__main__":
    print(app.url_map)
    app.run(host="0.0.0.0", port=5000, debug=True)
