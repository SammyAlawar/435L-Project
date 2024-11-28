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

def test_make_sale(client):

    response = client.post('/sales/purchase', json={
        'username': 'Slattyyyyyy',
        'good_name': 'test6',
        'category': 'electronics',
        'quantity': 1
    })
    assert response.status_code == 200
    assert 'Purchased' in response.json['message']

def test_make_sale_insufficient_stock(client):
    response = client.post('/sales/purchase', json={
        'username': 'Slattyyyyyy',
        'good_name': 'test6',
        'category': 'electronics',
        'quantity': 100
    })
    assert response.status_code == 400
    assert "Insufficient stock" in response.get_json()['error']


