"""
inventory_db.py
---------------
This module manages inventory operations, including adding, updating, and deducting stock,
retrieving product details, and ensuring data consistency.
"""

import sqlite3

def connect_to_db():
    """
    Connect to the SQLite database.

    Returns:
        sqlite3.Connection: The connection object to the SQLite database.
    """
    conn = sqlite3.connect('database.db')  # Replace 'database.db' with your desired database file
    return conn

def create_inventory_table():
    """
    Create the Inventory table if it does not exist.

    The table stores the following fields:
        - id: Unique identifier for each item.
        - name: Name of the item.
        - category: Category of the item ('food', 'clothes', 'accessories', 'electronics').
        - price_per_item: Price per unit of the item.
        - description: Additional information about the item.
        - stock_count: The quantity of the item available in stock.
    """
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL CHECK (category IN ('food', 'clothes', 'accessories', 'electronics')),
                price_per_item REAL NOT NULL,
                description TEXT,
                stock_count INTEGER NOT NULL,
                UNIQUE(name, category)
            );
        ''')
        conn.commit()
        print("Inventory table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()

def add_goods(goods):
    """
    Add a new item to the inventory.

    Args:
        goods (dict): A dictionary containing the item's details, including:
            - name (str): Name of the item.
            - category (str): Category of the item.
            - price_per_item (float): Price per unit of the item.
            - description (str): Description of the item.
            - stock_count (int): Quantity available in stock.

    Returns:
        dict: The newly added item's details, or an empty dictionary if an error occurs.
    """
    new_goods = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        goods['category'] = goods['category'].lower()
        goods['name'] = goods['name'].lower()

        cur.execute('''
            INSERT INTO Inventory (name, category, price_per_item, description, stock_count) 
            VALUES (?, ?, ?, ?, ?)
        ''', (
            goods['name'],
            goods['category'],
            goods['price_per_item'],
            goods['description'],
            goods['stock_count'],
        ))
        
        conn.commit()
        
        cur.execute("SELECT * FROM Inventory WHERE id = ?", (cur.lastrowid,))
        row = cur.fetchone()

        if row:
            new_goods = {
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "price_per_item": row[3],
                "description": row[4],
                "stock_count": row[5],
            }
    except sqlite3.Error as e:
        print(f"Error adding goods: {e}")
        conn.rollback()
    finally:
        conn.close()
    return new_goods

def deduct_goods(name, category, quantity):
    """
    Deduct a specified quantity from an item's stock.

    Args:
        name (str): The name of the item.
        category (str): The category of the item.
        quantity (int): The quantity to deduct.

    Returns:
        dict: The updated item's details if successful, or an error message if not.
    """
    updated_item = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        name = name.lower()
        category = category.lower()

        cur.execute("SELECT id, stock_count FROM Inventory WHERE name = ? AND category = ?", (name, category))
        item = cur.fetchone()

        if not item:
            return {"error": "Item not found."}

        item_id, current_stock = item

        if current_stock < quantity:
            return {"error": "Insufficient stock available."}

        new_stock = current_stock - quantity
        cur.execute("UPDATE Inventory SET stock_count = ? WHERE id = ?", (new_stock, item_id))
        conn.commit()

        cur.execute("SELECT * FROM Inventory WHERE id = ?", (item_id,))
        row = cur.fetchone()

        if row:
            updated_item = {
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "price_per_item": row[3],
                "description": row[4],
                "stock_count": row[5],
            }
    except sqlite3.Error as e:
        print(f"Error deducting goods: {e}")
        conn.rollback()
    finally:
        conn.close()
    return updated_item

def update_goods(name, category, updates):
    """
    Update the details of an item in the inventory.

    Args:
        name (str): The name of the item.
        category (str): The category of the item.
        updates (dict): A dictionary of fields to update and their new values.

    Returns:
        dict: The updated item's details if successful, or an error message if not.
    """
    updated_item = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        name = name.lower()
        category = category.lower()
        if 'name' in updates and updates['name']:
            updates['name'] = updates['name'].lower()
        if 'category' in updates and updates['category']:
            updates['category'] = updates['category'].lower()

        cur.execute("SELECT id FROM Inventory WHERE name = ? AND category = ?", (name, category))
        item = cur.fetchone()

        if not item:
            return {"error": "Item not found."}

        item_id = item[0]
        allowed_fields = {"name", "category", "price_per_item", "description", "stock_count"}
        invalid_fields = set(updates.keys()) - allowed_fields

        if invalid_fields:
            return {"error": f"Invalid fields: {', '.join(invalid_fields)}"}

        query = "UPDATE Inventory SET "
        query += ", ".join([f"{key} = ?" for key in updates.keys()])
        query += " WHERE id = ?"

        values = list(updates.values())
        values.append(item_id)

        cur.execute(query, values)
        conn.commit()

        cur.execute("SELECT * FROM Inventory WHERE id = ?", (item_id,))
        row = cur.fetchone()

        if row:
            updated_item = {
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "price_per_item": row[3],
                "description": row[4],
                "stock_count": row[5],
            }
    except sqlite3.Error as e:
        print(f"Error updating goods: {e}")
        conn.rollback()
    finally:
        conn.close()
    return updated_item

def get_all_goods():
    """
    Retrieve all items in the inventory.

    Returns:
        list: A list of dictionaries, each representing an item.
    """
    goods = []
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Inventory")
        rows = cur.fetchall()

        for row in rows:
            goods.append({
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "price_per_item": row[3],
                "description": row[4],
                "stock_count": row[5],
            })
    except sqlite3.Error as e:
        print(f"Error fetching goods: {e}")
    finally:
        conn.close()
    return goods

def get_good_by_name_and_category(name, category):
    """
    Retrieve a specific good by name and category.

    Args:
        name (str): The name of the good.
        category (str): The category of the good.

    Returns:
        dict: A dictionary representing the item if found, or an error message.
    """
    good = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        name = name.lower()
        category = category.lower()

        cur.execute("SELECT * FROM Inventory WHERE name = ? AND category = ?", (name, category))
        row = cur.fetchone()

        if row:
            good = {
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "price_per_item": row[3],
                "description": row[4],
                "stock_count": row[5],
            }
        else:
            return {"error": "Item not found."}
    except sqlite3.Error as e:
        print(f"Error fetching good by name and category: {e}")
    finally:
        conn.close()
    return good
