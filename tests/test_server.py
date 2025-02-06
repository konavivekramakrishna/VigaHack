import pytest
from app import app
from models.inventory import Inventory, db

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_function():
    with app.app_context():
        # Delete all rows in the Inventory table before each test
        db.session.query(Inventory).delete()
        db.session.commit()

def test_add_item_route(client):
    data = {"name": "Test Item", "quantity": 10}
    response = client.post('/add-item', json=data)
    assert response.status_code == 201
    assert response.json["message"] == "Item added successfully"

def test_get_items_route(client):
    # Get initial items
    initial_response = client.get('/get-items')
    initial_length = len(initial_response.json["data"])

    # Add some items
    client.post('/add-item', json={"name": "Item 1", "quantity": 10})
    client.post('/add-item', json={"name": "Item 2", "quantity": 5})

    # Get new items
    response = client.get('/get-items')
    new_length = len(response.json["data"])

    assert response.status_code == 200
    assert new_length == initial_length + 2
    assert "Item 1" in [item["name"] for item in response.json["data"]]
    assert "Item 2" in [item["name"] for item in response.json["data"]]

def test_remove_item_route(client):
    # First, add the item
    client.post('/add-item', json={"name": "Test Item", "quantity": 10})
    
    data = {"name": "Test Item"}
    response = client.delete('/remove-item', json=data)
    assert response.status_code == 200
    assert response.json["message"] == "Item removed successfully"

def test_update_quantity_route(client):
    # First, add the item
    client.post('/add-item', json={"name": "Test Item", "quantity": 10})
    # Update the quantity
    data = {"name": "Test Item", "quantity": 20}
    response = client.put('/update-quantity', json=data)
    assert response.status_code == 200
    assert response.json["message"] == "Quantity updated successfully"

def test_add_item_already_exists(client):
    # Add an item
    client.post('/add-item', json={"name": "Item 1", "quantity": 10})

    # Try to add the same item again
    response = client.post('/add-item', json={"name": "Item 1", "quantity": 10})
    assert response.status_code == 400
    assert response.json["error"] == "Item already exists"

def test_remove_item_not_exists(client):
    # Try to remove an item that does not exist
    response = client.delete('/remove-item', json={"name": "Nonexistent Item"})
    assert response.status_code == 404
    assert response.json["error"] == "Item not found"

def test_update_quantity_item_not_exists(client):
    # Try to update the quantity of an item that does not exist
    response = client.put('/update-quantity', json={"name": "Nonexistent Item", "quantity": 10})
    assert response.status_code == 404
    assert response.json["error"] == "Item not found"



__table_args__ = {'extend_existing': True}
