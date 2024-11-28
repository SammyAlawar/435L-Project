import pytest
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_goods(client):
    response = client.post('/inventory/add_goods', json={
        'name': 'test6',
        'category': 'electronics',
        'price_per_item': 50000,
        'description': 'This is a test6',
        'stock_count': 50
    })
    assert response.status_code == 201
    assert 'name' in response.get_json()

def test_get_goods_by_name_and_category(client):
    response = client.get('/inventory/get_goods/test6/electronics')
    assert response.status_code == 200
    assert response.json['name'] == 'test6'

def test_deduct_goods(client):
    response = client.post('/inventory/deduct_goods/test6/electronics/5')
    assert response.status_code == 200
    assert response.json['stock_count'] == 45

def test_update_goods(client):
    response = client.put('/inventory/update_goods/update', json={
        'name': 'test6',
        'category': 'electronics',
        'updates': {'price_per_item': 20, 'description': 'Updated description'}
    })
    assert response.status_code == 200
    assert "updated successfully" in response.get_json()['message']

def test_update_goods_invalid_input(client):
    response = client.put('/inventory/update_goods/update', json={
        'name': '',
        'category': '',
        'updates': {'price_per_item': 20}
    })
    assert response.status_code == 400
    assert "Invalid input" in response.get_json()['error']

def test_get_good_not_found(client):
    response = client.get('/inventory/get_goods/nonexistent/electronics')
    assert response.status_code == 404
    assert "Item not found" in response.get_json()['error']

def test_add_goods_duplicate(client):
    response = client.post('/inventory/add_goods', json={
        'name': 'test6',
        'category': 'electronics',  # Duplicate name and category
        'price_per_item': 10,
        'description': 'This is a test6',
        'stock_count': 50
    })
    assert response.status_code == 500
    assert "error" in response.get_json()

def test_get_goods_not_found(client):
    response = client.get('/inventory/get_goods/nonexistent/electronics')
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_deduct_goods_insufficient_stock(client):
    response = client.post('/inventory/deduct_goods/test6/electronics/1000')  # Exceeds stock count
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_update_nonexistent_goods(client):
    response = client.put('/inventory/update_goods/update', json={
        'name': 'nonexistentitem',
        'category': 'electronics',
        'updates': {'price_per_item': 100}
    })
    assert response.status_code == 404
    assert "not found" in response.get_json()['error']

def test_deduct_insufficient_stock(client):
    response = client.post('/inventory/deduct_goods/test6/electronics/1000')
    assert response.status_code == 400
    assert "Insufficient stock available" in response.get_json()['error']

def test_add_invalid_goods(client):
    response = client.post('/inventory/add_goods', json={
        'name': 'test_invalid',
        # Missing category, price_per_item, description, stock_count
    })
    assert response.status_code == 400
    assert "Missing fields" in response.get_json()['error']

def test_add_goods_invalid_stock_count(client):
    response = client.post('/inventory/add_goods', json={
        'name': 'InvalidItem',
        'category': 'InvalidCategory',
        'price_per_item': 100,
        'description': 'Invalid test item',
        'stock_count': -1  # Negative stock count
    })
    assert response.status_code == 400
    assert "Invalid value for 'stock_count'" in response.get_json()['error']

def test_add_goods_missing_fields(client):
    response = client.post('/inventory/add_goods', json={
        'name': 'Laptop',
        'category': 'Electronics',
        # Missing 'price_per_item', 'description', 'stock_count'
    })
    assert response.status_code == 400
    assert "Missing fields" in response.get_json()['error']

def test_add_goods_invalid_price(client):
    response = client.post('/inventory/add_goods', json={
        'name': 'Laptop',
        'category': 'Electronics',
        'price_per_item': -1000,  # Invalid price
        'description': 'A high-end laptop',
        'stock_count': 10
    })
    assert response.status_code == 400
    assert "Invalid price_per_item" in response.get_json()['error']

def test_add_goods_invalid_stock_count(client):
    response = client.post('/inventory/add_goods', json={
        'name': 'Laptop',
        'category': 'Electronics',
        'price_per_item': 1000,
        'description': 'A high-end laptop',
        'stock_count': -5  # Invalid stock count
    })
    assert response.status_code == 400
    assert "Invalid stock_count" in response.get_json()['error']
