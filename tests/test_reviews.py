import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_submit_review(client):
    response = client.post('/reviews/submit', json={
        'product_name': 'test6',
        'username': 'Slattyyyyyy',
        'rating': 5,
        'comment': 'Amazing!'
    })
    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data['rating'] == 5
    assert "Successfully submitted 5 star review." in response_data['message']


def test_get_product_reviews(client):
    response = client.get('/reviews/product/test6')
    assert response.status_code == 200
    assert len(response.get_json()) > 0

def test_update_review(client):
    response = client.put('/reviews/update/1', json={
        'rating': 4,
        'comment': 'Updated comment'
    })
    assert response.status_code == 200
    assert "Review updated successfully" in response.get_json()['message']

def test_update_review_invalid_rating(client):
    response = client.put('/reviews/update/1', json={
        'rating': 6,
        'comment': 'Invalid rating'
    })
    assert response.status_code == 400
    assert "Rating must be between 1 and 5" in response.get_json()['error']

def test_moderate_review(client):
    response = client.patch('/reviews/moderate/1', json={'moderated': True})
    assert response.status_code == 200
    assert "Review moderation updated successfully" in response.get_json()['message']

def test_submit_review_invalid_rating(client):
    response = client.post('/reviews/submit', json={
        'product_name': 'test6',
        'username': 'Slattyyyyyy',
        'rating': 10,  # Invalid rating
        'comment': 'Amazing!'
    })
    assert response.status_code == 400
    assert "Invalid input" in response.get_json()['error']


