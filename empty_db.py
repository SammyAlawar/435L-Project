import sqlite3

def empty_database():
    conn = sqlite3.connect('database.db')
    try:
        cursor = conn.cursor()
        # List all your table names here
        tables = ["Customers", "Inventory", "PurchaseHistory", "Reviews"]

        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")  # Reset auto-increment ID
        conn.commit()
        print("All tables emptied successfully.")
    except sqlite3.Error as e:
        print(f"Error emptying database: {e}")
    finally:
        conn.close()

# Call the function
empty_database()
