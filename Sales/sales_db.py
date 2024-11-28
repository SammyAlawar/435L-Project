"""
sales_db.py
-----------
This module tracks sales operations, manages customer purchases, handles transactions, and saves purchase history for reporting purposes.
"""
import sqlite3

def connect_to_db():
    """
    Connect to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to interact with the database.
    """
    return sqlite3.connect('database.db')

def create_purchase_history_table():
    """
    Create the 'PurchaseHistory' table if it does not exist.

    This table stores details of purchases made by users, including:
    - `id`: Unique identifier for each purchase record.
    - `username`: The username of the customer making the purchase.
    - `good_name`: The name of the purchased item.
    - `quantity`: The number of items purchased.
    - `total_cost`: The total cost of the purchase.
    - `purchase_date`: The timestamp of the purchase.
    """
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS PurchaseHistory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                good_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                total_cost REAL NOT NULL,
                purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        print("PurchaseHistory table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating purchase history table: {e}")
    finally:
        conn.close()

def save_purchase_history(username, good_name, quantity, total_cost):
    """
    Save a purchase record to the 'PurchaseHistory' table.

    Args:
        username (str): The username of the customer making the purchase.
        good_name (str): The name of the purchased item.
        quantity (int): The number of items purchased.
        total_cost (float): The total cost of the purchase.

    Raises:
        sqlite3.Error: If there is an error during the database operation.

    Example:
        save_purchase_history("john_doe", "Laptop", 1, 1500.0)
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO PurchaseHistory (username, good_name, quantity, total_cost)
            VALUES (?, ?, ?, ?)
        ''', (username, good_name, quantity, total_cost))
        conn.commit()
        print("Purchase history saved successfully.")
    except sqlite3.Error as e:
        print(f"Error saving purchase history: {e}")
        conn.rollback()
    finally:
        conn.close()
