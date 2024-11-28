from memory_profiler import profile
from app import app

@profile
def test_register_customer_memory():
    """
    Test the memory usage of the customer registration API.
    """
    # Simulating a Flask request
    with app.test_client() as client:
        customer_data = {
            'full_name': 'Test User',
            'username': 'testuser',
            'password': 'securepassword',
            'age': 30,
            'address': '123 Test St',
            'gender': 'male',
            'marital_status': 'single',
            'wallet': 1000
        }
        response = client.post('/customers/register', json=customer_data)
        print(response.json)

if __name__ == '__main__':
    test_register_customer_memory()
