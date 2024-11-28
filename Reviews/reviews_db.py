"""
reviews_db.py
-------------
This module manages customer reviews, including submitting, updating, deleting, moderating reviews, and retrieving review details.
"""

import sqlite3
from datetime import datetime

def connect_to_db():
    """
    Connect to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to interact with the database.
    """
    return sqlite3.connect('database.db')

def create_reviews_table():
    """
    Create the Reviews table if it does not exist.

    The table stores product reviews, including product name, username, rating, and comments.
    """
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                username TEXT NOT NULL,
                rating INTEGER CHECK(rating BETWEEN 1 AND 5) NOT NULL,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                moderated BOOLEAN DEFAULT 0
            );
        ''')
        conn.commit()
        print("Reviews table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating reviews table: {e}")
    finally:
        conn.close()

def validate_review_input(rating):
    """
    Validate the rating value.

    Args:
        rating (int): The rating value to validate.

    Raises:
        ValueError: If the rating is not between 1 and 5.
    """
    if not (1 <= rating <= 5):
        raise ValueError("Rating must be an integer between 1 and 5.")

def submit_review(product_name, username, rating, comment):
    """
    Submit a new review for a product.

    Args:
        product_name (str): The name of the product.
        username (str): The username of the reviewer.
        rating (int): The rating given to the product (1-5).
        comment (str): The review comment.

    Returns:
        dict: A success message or an error message.
    """
    try:
        validate_review_input(rating)
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO Reviews (product_name, username, rating, comment) 
            VALUES (?, ?, ?, ?)
        ''', (product_name.strip(), username.strip(), rating, comment.strip()))
        conn.commit()
        return {"message": "Review submitted successfully."}
    except ValueError as ve:
        return {"error": str(ve)}
    except sqlite3.Error as e:
        return {"error": f"Error submitting review: {e}"}
    finally:
        conn.close()

def update_review(review_id, rating, comment):
    """
    Update an existing review.

    Args:
        review_id (int): The ID of the review to update.
        rating (int): The updated rating (1-5).
        comment (str): The updated comment.

    Returns:
        dict: A success message or an error message.
    """
    try:
        validate_review_input(rating)
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            UPDATE Reviews SET rating = ?, comment = ? WHERE id = ?
        ''', (rating, comment.strip(), review_id))
        conn.commit()
        return {"message": "Review updated successfully."}
    except ValueError as ve:
        return {"error": str(ve)}
    except sqlite3.Error as e:
        return {"error": f"Error updating review: {e}"}
    finally:
        conn.close()

def delete_review(review_id):
    """
    Delete a review by ID.

    Args:
        review_id (int): The ID of the review to delete.

    Returns:
        dict: A success message or an error message.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            DELETE FROM Reviews WHERE id = ?
        ''', (review_id,))
        conn.commit()
        return {"message": "Review deleted successfully."}
    except sqlite3.Error as e:
        return {"error": f"Error deleting review: {e}"}
    finally:
        conn.close()

def get_product_reviews(product_name):
    """
    Get all reviews for a specific product.

    Args:
        product_name (str): The name of the product.

    Returns:
        list: A list of reviews or an error message.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            SELECT * FROM Reviews WHERE product_name = ? AND moderated = 0
        ''', (product_name.strip(),))
        reviews = cur.fetchall()
        return [{"id": row[0], "username": row[2], "rating": row[3], "comment": row[4], "created_at": row[5]} for row in reviews]
    except sqlite3.Error as e:
        return {"error": f"Error fetching reviews: {e}"}
    finally:
        conn.close()

def get_customer_reviews(username):
    """
    Get all reviews submitted by a specific customer.

    Args:
        username (str): The username of the customer.

    Returns:
        list: A list of reviews or an error message.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            SELECT * FROM Reviews WHERE username = ?
        ''', (username.strip(),))
        reviews = cur.fetchall()
        return [{"id": row[0], "product_name": row[1], "rating": row[3], "comment": row[4], "created_at": row[5]} for row in reviews]
    except sqlite3.Error as e:
        return {"error": f"Error fetching customer reviews: {e}"}
    finally:
        conn.close()

def moderate_review(review_id, moderated):
    """
    Moderate a review by updating its status.

    Args:
        review_id (int): The ID of the review to moderate.
        moderated (bool): The moderation status (True for approved, False for flagged).

    Returns:
        dict: A success message or an error message.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            UPDATE Reviews SET moderated = ? WHERE id = ?
        ''', (moderated, review_id))
        conn.commit()
        return {"message": "Review moderation updated successfully."}
    except sqlite3.Error as e:
        return {"error": f"Error moderating review: {e}"}
    finally:
        conn.close()

def get_review_details(review_id):
    """
    Get the details of a specific review.

    Args:
        review_id (int): The ID of the review.

    Returns:
        dict: A dictionary with review details or an error message.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            SELECT * FROM Reviews WHERE id = ?
        ''', (review_id,))
        row = cur.fetchone()
        if row:
            return {"id": row[0], "product_name": row[1], "username": row[2], "rating": row[3], "comment": row[4], "created_at": row[5], "moderated": row[6]}
        return {"error": "Review not found."}
    except sqlite3.Error as e:
        return {"error": f"Error fetching review details: {e}"}
    finally:
        conn.close()
