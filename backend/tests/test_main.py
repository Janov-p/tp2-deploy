import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_hello_endpoint(client):
    """Test the hello endpoint returns correct response"""
    response = client.get('/hello')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Hello, World!'
    assert data['status'] == 'success' 