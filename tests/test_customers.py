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

def test_register_customer(client):
    response = client.post('/customers/register', json={
        'full_name': 'Test Testing',
        'username': 'Slattyyyyyy',
        'password': 'securepassword',
        'age': 30,
        'address': '123 Main Street',
        'gender': 'male',
        'marital_status': 'single',
        'wallet': 10000
    })
    assert response.status_code == 201
    assert 'username' in response.get_json()

def test_charge_wallet(client):
    response = client.post('/customers/get_customer/Slattyyyyyy/charge/5000')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['wallet'] > 0
    assert "Charged $5000 to 'Slattyyyyyy' wallet successfully" in response_data['message']

def test_get_all_customers(client):
    response = client.get('/customers/get_all_customers')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_customer_by_username(client):
    response = client.get('/customers/get_customer/Slattyyyyyy')
    assert response.status_code == 200
    assert 'username' in response.get_json()

def test_get_customer_not_found(client):
    response = client.get('/customers/get_customer/NonExistentUser')
    assert response.status_code == 404
    assert 'error' in response.get_json()

def test_deduct_wallet(client):
    response = client.post('/customers/get_customer/Slattyyyyyy/deduct/500')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['wallet'] >= 0
    assert "Deducted $500" in response_data['message']

def test_deduct_wallet_insufficient_balance(client):
    response = client.post('/customers/get_customer/Slattyyyyyy/deduct/1000000')
    assert response.status_code == 400
    assert "insufficient balance" in response.get_json()['error']


def test_get_customer_wallet(client):
    response = client.get('/customers/get_customer/Slattyyyyyy')
    assert response.status_code == 200
    assert 'wallet' in response.get_json()

def test_register_customer_duplicate(client):
    response = client.post('/customers/register', json={
        'full_name': 'Test Testing',
        'username': 'Slattyyyyyy',  # Duplicate username
        'password': 'securepassword',
        'age': 30,
        'address': '123 Main Street',
        'gender': 'male',
        'marital_status': 'single',
        'wallet': 10000
    })
    assert response.status_code == 409
    assert "error" in response.get_json()

def test_delete_nonexistent_customer(client):
    response = client.delete('/customers/delete/nonexistentuser')
    assert response.status_code == 404
  
def test_get_customer_by_username_not_found(client):
    response = client.get('/customers/get_customer/nonexistentuser')
    assert response.status_code == 404
    assert "Customer not found" in response.get_json()['error']

def test_charge_wallet_invalid_amount(client):
    response = client.post('/customers/get_customer/Slattyyyyyy/charge/-500')
    assert response.status_code == 400
    assert "Amount must be greater than zero" in response.get_json()['error']

def test_delete_customer_error(client):
    response = client.delete('/customers/delete/erroruser')
    assert response.status_code == 404
    assert "Customer not found" in response.get_json()['error']

def test_get_nonexistent_customer(client):
    response = client.get('/customers/get_customer/nonexistentuser')
    assert response.status_code == 404
    assert "Customer not found" in response.get_json()['error']

def test_charge_wallet_invalid_amount(client):
    response = client.post('/customers/get_customer/Slattyyyyyy/charge/-500')
    assert response.status_code == 400
    assert "Amount must be greater than zero" in response.get_json()['error']

def test_deduct_wallet_insufficient_balance(client):
    response = client.post('/customers/get_customer/Slattyyyyyy/deduct/1000000')
    assert response.status_code == 400
    assert "insufficient balance" in response.get_json()['error']

def test_delete_nonexistent_customer(client):
    response = client.delete('/customers/delete/nonexistentuser')
    assert response.status_code == 404
    assert "Customer not found" in response.get_json()['error']

def test_register_customer_missing_fields(client):
    response = client.post('/customers/register', json={
        'username': 'MissingFields',  # Missing fields like 'full_name', 'password', etc.
    })
    assert response.status_code == 400
    assert "error" in response.get_json()
def test_register_customer_missing_fields(client):
    # Missing 'address' field
    response = client.post('/customers/register', json={
        'full_name': 'Test User',
        'username': 'user_missing_field',
        'password': 'password123',
        'age': 25,
        'gender': 'male',
        'marital_status': 'single',
        'wallet': 100
    })
    assert response.status_code == 400
    assert "Missing fields: address" in response.get_json()['error']

def test_register_customer_invalid_age(client):
    response = client.post('/customers/register', json={
        'full_name': 'Test User',
        'username': 'user_invalid_age',
        'password': 'password123',
        'age': -5,  # Invalid age
        'address': '123 Fake Street',
        'gender': 'male',
        'marital_status': 'single',
        'wallet': 100
    })
    assert response.status_code == 400
    assert "Invalid age" in response.get_json()['error']

def test_register_customer_invalid_wallet(client):
    response = client.post('/customers/register', json={
        'full_name': 'Test User',
        'username': 'user_invalid_wallet',
        'password': 'password123',
        'age': 25,
        'address': '123 Fake Street',
        'gender': 'male',
        'marital_status': 'single',
        'wallet': -50  # Invalid wallet
    })
    assert response.status_code == 400
    assert "Invalid wallet value" in response.get_json()['error']
