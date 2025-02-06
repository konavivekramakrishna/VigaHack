import pytest
from app import app
from models.inventory import Inventory, db

@pytest.fixture
def client():
    """
    Creates a test client for the Flask application.
    Returns:
        client: A Flask test client instance.
    """
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_function():
    """
    Clears the Inventory table before each test to ensure a clean state.
    """
    with app.app_context():
        db.session.query(Inventory).delete()
        db.session.commit()

def test_add_item_route(client):
    """
    Tests the /add-item endpoint by adding a new item.
    Parameters:
        client: Flask test client.
    Returns:
        None
    """
    data = {"name": "Test Item", "quantity": 10}
    response = client.post('/add-item', json=data)
    assert response.status_code == 201
    assert response.json["message"] == "Item added successfully"

def test_get_items_route(client):
    """
    Tests the /get-items endpoint to retrieve all items in the inventory.
    Parameters:
        client: Flask test client.
    Returns:
        None
    """
    initial_response = client.get('/get-items')
    initial_length = len(initial_response.json["data"])

    client.post('/add-item', json={"name": "Item 1", "quantity": 10})
    client.post('/add-item', json={"name": "Item 2", "quantity": 5})

    response = client.get('/get-items')
    new_length = len(response.json["data"])

    assert response.status_code == 200
    assert new_length == initial_length + 2
    assert "Item 1" in [item["name"] for item in response.json["data"]]
    assert "Item 2" in [item["name"] for item in response.json["data"]]

def test_remove_item_route(client):
    """
    Tests the /remove-item endpoint by deleting an existing item.
    Parameters:
        client: Flask test client.
    Returns:
        None
    """
    client.post('/add-item', json={"name": "Test Item", "quantity": 10})
    data = {"name": "Test Item"}
    response = client.delete('/remove-item', json=data)
    assert response.status_code == 200
    assert response.json["message"] == "Item removed successfully"

def test_update_quantity_route(client):
    """
    Tests the /update-quantity endpoint by updating an item's quantity.
    Parameters:
        client: Flask test client.
    Returns:
        None
    """
    client.post('/add-item', json={"name": "Test Item", "quantity": 10})
    data = {"name": "Test Item", "quantity": 20}
    response = client.put('/update-quantity', json=data)
    assert response.status_code == 200
    assert response.json["message"] == "Quantity updated successfully"

def test_add_item_already_exists(client):
    """
    Tests that adding an item with an existing name returns a 400 error.
    Parameters:
        client: Flask test client.
    Returns:
        None
    """
    client.post('/add-item', json={"name": "Item 1", "quantity": 10})
    response = client.post('/add-item', json={"name": "Item 1", "quantity": 10})
    assert response.status_code == 400
    assert response.json["error"] == "Item already exists"

def test_remove_item_not_exists(client):
    """
    Tests that trying to remove a nonexistent item returns a 404 error.
    Parameters:
        client: Flask test client.
    Returns:
        None
    """
    response = client.delete('/remove-item', json={"name": "Nonexistent Item"})
    assert response.status_code == 404
    assert response.json["error"] == "Item not found"

def test_update_quantity_item_not_exists(client):
    """
    Tests that trying to update the quantity of a nonexistent item returns a 404 error.
    Parameters:
        client: Flask test client.
    Returns:
        None
    """
    response = client.put('/update-quantity', json={"name": "Nonexistent Item", "quantity": 10})
    assert response.status_code == 404
    assert response.json["error"] == "Item not found"
