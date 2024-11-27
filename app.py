from flask import Flask, request, jsonify
from flask_cors import CORS
from Customers.customers_db import (
    create_customers_table,
    register_customer,
    delete_customer,
    update_customer,
    get_all_customers,
    get_customer_by_username,
    charge_customer_wallet,
    deduct_customer_wallet
)


# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests

# Ensure the Customers table exists
create_customers_table()

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Customer Management API!"})

# GET: Retrieve all customers
@app.route('/customers/get_all_customers', methods=['GET'])
def api_get_all_customers():
    customers = get_all_customers()
    return jsonify(customers)

# GET: Retrieve a customer by username
@app.route('/customers/get_customer/<string:username>', methods=['GET'])
def api_get_customer_by_username(username):
    customer = get_customer_by_username(username)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer)

# POST: Register a new customer
@app.route('/customers/register', methods=['POST'])
def api_register_customer():
    customer = request.get_json()
    if not customer:
        return jsonify({"error": "Invalid input"}), 400

    registered_customer = register_customer(customer)
    if not registered_customer:
        return jsonify({"error": "Could not register customer"}), 500
    return jsonify(registered_customer), 201

# DELETE: Delete a customer by username
@app.route('/customers/delete/<string:username>', methods=['DELETE'])
def api_delete_customer(username):
    success = delete_customer(username)
    if not success:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify({"message": f"Customer '{username}' deleted successfully."})

# PUT: Update a customer's information
@app.route('/customers/update/<string:username>', methods=['PUT'])
def api_update_customer(username):
    updates = request.get_json()
    if not updates:
        return jsonify({"error": "Invalid input"}), 400

    success = update_customer(username, updates)
    if not success:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify({"message": f"Customer '{username}' updated successfully."})

# POST: Charge customer wallet
from flask import Flask, request, jsonify

@app.route('/customers/get_customer/<string:username>/charge/<int:amount>', methods=['POST'])
def api_charge_wallet(username, amount):
    """
    API to charge a specified amount to a customer's wallet.
    """
    if amount <= 0:
        return jsonify({"error": "Amount must be greater than zero"}), 400

    # Call the charge_customer_wallet function
    success = charge_customer_wallet(username, amount)
    
    if not success:
        return jsonify({"error": "Customer not found or could not charge wallet"}), 404
    
    return jsonify({"message": f"Charged ${amount} to '{username}' wallet successfully."})


# POST: Deduct from customer wallet
@app.route('/customers/get_customer/<string:username>/deduct/<int:amount>', methods=['POST'])
def api_deduct_wallet(username, amount):
    """
    API to deduct a specified amount from a customer's wallet.
    """
    if amount <= 0:
        return jsonify({"error": "Amount must be greater than zero"}), 400

    success = deduct_customer_wallet(username, amount)
    if not success:
        return jsonify({"error": "Customer not found, insufficient balance, or could not deduct wallet"}), 400
    
    return jsonify({"message": f"Deducted ${amount} from '{username}' wallet successfully."})




'''APIs for Inventory'''

from Inventory.inventory_db import (
    create_inventory_table,
    add_goods,
    deduct_goods,
    update_goods,
    get_all_goods,
    get_good_by_name_and_category
)

create_inventory_table()

@app.route('/inventory/add_goods', methods=['POST'])
def api_add_goods():
    goods = request.get_json()
    if not goods:
        return jsonify({"error": "Invalid input"}), 400

    added_goods = add_goods(goods)
    if not added_goods:
        return jsonify({"error": "Could not register goods"}), 500
    return jsonify(added_goods), 201

@app.route('/inventory/deduct_goods/<string:name>/<string:category>/<int:quantity>', methods=['POST'])
def api_deduct_goods(name, category, quantity):
    """
    API to deduct a quantity from an item's stock in the inventory.
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
    """
    data = request.get_json()

    # Validate input
    name = data.get('name')
    category = data.get('category')
    updates = data.get('updates')

    if not name or not category or not updates:
        return jsonify({"error": "Invalid input. Name, category, and updates are required."}), 400

    # Call the update_goods function
    result = update_goods(name, category, updates)

    # Handle the result
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 200

@app.route('/inventory/get_all_goods', methods=['GET'])
def api_get_all_goods():
    goods = get_all_goods()
    return jsonify(goods), 200

@app.route('/inventory/get_goods/<string:name>/<string:category>', methods=['GET'])
def api_get_good_by_name_and_category(name, category):
    """
    API to retrieve a specific good by name and category.
    """
    good = get_good_by_name_and_category(name, category)
    if "error" in good:
        return jsonify(good), 404
    return jsonify(good), 200

# Run the application
if __name__ == "__main__":
    app.run(debug=True, port=5000)
