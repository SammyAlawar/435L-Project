"""
customers_db.py
---------------
This module handles all customer-related operations, such as registration, wallet management, and updates.
"""
import sqlite3
def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_customers_table():
    """Create the Customers table if it does not exist."""
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                age INTEGER NOT NULL,
                address TEXT NOT NULL,
                gender TEXT NOT NULL,
                marital_status TEXT NOT NULL,
                wallet REAL DEFAULT 0.0
            );
        ''')
        conn.commit()  # Save changes to the database
        print("Customers table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()

def register_customer(customer):
    """
    Registers a new customer in the Customers table.
    
    Args:
        customer (dict): A dictionary containing customer details.
    
    Returns:
        dict: A dictionary containing the inserted customer's details, or an empty dictionary if an error occurred.
    """
    registered_customer = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Insert the new customer into the database
        cur.execute('''
            INSERT INTO Customers (full_name, username, password, age, address, gender, marital_status, wallet) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            customer['full_name'],
            customer['username'],
            customer['password'],
            customer['age'],
            customer['address'],
            customer['gender'],
            customer['marital_status'],
            customer['wallet']
        ))
        
        conn.commit()  # Commit the transaction
        
        # Retrieve the inserted customer using the last inserted row ID
        cur.execute("SELECT * FROM Customers WHERE id = ?", (cur.lastrowid,))
        row = cur.fetchone()
        
        # Map the row to a dictionary
        if row:
            registered_customer = {
                "id": row[0],
                "full_name": row[1],
                "username": row[2],
                "password": row[3],
                "age": row[4],
                "address": row[5],
                "gender": row[6],
                "marital_status": row[7],
                "wallet": row[8]
            }
    except sqlite3.Error as e:
        print(f"Error registering customer: {e}")
        conn.rollback()  # Roll back the transaction if an error occurs
    finally:
        conn.close()  # Ensure the database connection is always closed
    return registered_customer

def delete_customer(username):
    """
    Deletes a customer by username.
    
    Args:
        username (str): The username of the customer to delete.
    
    Returns:
        bool: True if the customer was deleted, False if no customer was found.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Check if the customer exists
        cur.execute("SELECT * FROM Customers WHERE username = ?", (username,))
        customer = cur.fetchone()
        if not customer:
            return False  # No customer found with the given username

        # Delete the customer
        cur.execute("DELETE FROM Customers WHERE username = ?", (username,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting customer: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def update_customer(username, updates):
    """
    Updates one or more fields of a customer by username.
    
    Args:
        username (str): The username of the customer to update.
        updates (dict): A dictionary containing the fields to update and their new values.
    
    Returns:
        bool: True if the customer was updated, False if no customer was found.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Check if the customer exists
        cur.execute("SELECT * FROM Customers WHERE username = ?", (username,))
        customer = cur.fetchone()
        if not customer:
            return False  # No customer found with the given username

        # Build the SQL query dynamically based on updates
        query = "UPDATE Customers SET "
        query += ", ".join([f"{key} = ?" for key in updates.keys()])
        query += " WHERE username = ?"
        
        # Execute the query with values
        values = list(updates.values())
        values.append(username)
        cur.execute(query, values)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating customer: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_all_customers():
    """
    Retrieves all customers from the database.
    
    Returns:
        list: A list of dictionaries, each representing a customer.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Fetch all customers
        cur.execute("SELECT * FROM Customers")
        rows = cur.fetchall()

        # Map rows to dictionaries
        customers = []
        for row in rows:
            customers.append({
                "id": row[0],
                "full_name": row[1],
                "username": row[2],
                "password": row[3],
                "age": row[4],
                "address": row[5],
                "gender": row[6],
                "marital_status": row[7],
                "wallet": row[8],
            })
        return customers
    except sqlite3.Error as e:
        print(f"Error fetching customers: {e}")
        return []
    finally:
        conn.close()

def get_customer_by_username(username):
    """
    Retrieves a customer by their username.
    
    Args:
        username (str): The unique username of the customer.
    
    Returns:
        dict: A dictionary containing the customer's details, or None if not found.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Fetch the customer
        cur.execute("SELECT * FROM Customers WHERE username = ?", (username,))
        row = cur.fetchone()

        # Map row to dictionary
        if row:
            return {
                "id": row[0],
                "full_name": row[1],
                "username": row[2],
                "password": row[3],
                "age": row[4],
                "address": row[5],
                "gender": row[6],
                "marital_status": row[7],
                "wallet": row[8],
            }
        return None
    except sqlite3.Error as e:
        print(f"Error fetching customer by username: {e}")
        return None
    finally:
        conn.close()

def charge_customer_wallet(username, amount):
    """
    Charges a customer's wallet by adding a specified amount.
    
    Args:
        username (str): The username of the customer.
        amount (float): The amount to add to the wallet.
    
    Returns:
        bool: True if successful, False if the customer is not found or an error occurs.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Check if the customer exists
        cur.execute("SELECT wallet FROM Customers WHERE username = ?", (username,))
        customer = cur.fetchone()
        if not customer:
            return False  # Customer not found

        # Update the wallet
        new_balance = customer[0] + amount
        cur.execute("UPDATE Customers SET wallet = ? WHERE username = ?", (new_balance, username))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error charging wallet: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def deduct_customer_wallet(username, amount):
    """
    Deducts a specified amount from a customer's wallet.
    
    Args:
        username (str): The username of the customer.
        amount (float): The amount to deduct from the wallet.
    
    Returns:
        bool: True if successful, False if the customer is not found, insufficient balance, or an error occurs.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Check if the customer exists
        cur.execute("SELECT wallet FROM Customers WHERE username = ?", (username,))
        customer = cur.fetchone()
        if not customer:
            return False  # Customer not found

        # Check if the wallet has sufficient balance
        if customer[0] < amount:
            print("Insufficient wallet balance.")
            return False

        # Deduct the amount
        new_balance = customer[0] - amount
        cur.execute("UPDATE Customers SET wallet = ? WHERE username = ?", (new_balance, username))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deducting wallet: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_customer_wallet(username):
    """
    Retrieves the wallet balance of a customer by their username.
    
    Args:
        username (str): The unique username of the customer.
    
    Returns:
        float: The wallet balance of the customer, or None if the customer is not found.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Fetch the customer's wallet balance
        cur.execute("SELECT wallet FROM Customers WHERE username = ?", (username,))
        wallet = cur.fetchone()

        # Check if the customer exists
        if wallet:
            return wallet[0]
        return None
    except sqlite3.Error as e:
        print(f"Error fetching wallet balance: {e}")
        return None
    finally:
        conn.close()
