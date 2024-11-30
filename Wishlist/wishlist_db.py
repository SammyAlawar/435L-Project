import sqlite3

# Create Wishlist table
def create_wishlist_table():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Wishlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(customer_id) REFERENCES Customers(id),
            FOREIGN KEY(product_id) REFERENCES Inventory(id)
        )
    ''')
    conn.commit()
    conn.close()

# Add a product to the wishlist
def add_to_wishlist(customer_id, product_id):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Wishlist (customer_id, product_id)
        VALUES (?, ?)
    ''', (customer_id, product_id))
    conn.commit()
    conn.close()

# Remove a product from the wishlist
def remove_from_wishlist(customer_id, product_id):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM Wishlist
        WHERE customer_id = ? AND product_id = ?
    ''', (customer_id, product_id))
    conn.commit()
    conn.close()

# Fetch all products in a customer's wishlist
def get_wishlist(customer_id):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Inventory.name, Inventory.category, Inventory.price_per_item, Wishlist.added_on
        FROM Wishlist
        JOIN Inventory ON Wishlist.product_id = Inventory.id
        WHERE Wishlist.customer_id = ?
    ''', (customer_id,))
    wishlist = cursor.fetchall()
    conn.close()
    return wishlist
