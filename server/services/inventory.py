from database import db
from models.inventory import Inventory


def get_items():
    """
    Retrieves all items from the inventory.

    Parameters:
    - None.

    Returns:
    - A tuple (success, result):
      - success (bool): True if the operation was successful, False if an error occurred.
      - result (list or str): A list of dictionaries containing item names and quantities if successful,
                              or an error message if there was an issue.
    """
    try:
        items = Inventory.query.all()

        items_list = [{"name": item.name, "quantity": item.quantity} for item in items]

        return True, items_list if items_list else []
    except Exception as e:
        return False, f"Error getting items: {str(e)}"


def add_item(name, quantity):
    """
    Adds a new item to the inventory.

    Parameters:
    - name (str): The name of the item to be added.
    - quantity (int): The quantity of the item to be added.

    Returns:
    - A tuple (success, result):
      - success (bool): True if the item was added successfully, False if an error occurred.
      - result (dict or str): A dictionary containing the item's name and quantity if successful,
                              or an error message if there was an issue.
    """
    try:
        if not isinstance(quantity, int):
            return False, "Quantity must be an integer"

        if Inventory.query.filter_by(name=name).first():
            return False, "Item already exists"

        new_item = Inventory(name=name, quantity=quantity)
        db.session.add(new_item)
        db.session.commit()
        return True, {"name": name, "quantity": quantity}
    except Exception as e:
        return False, f"Error adding item: {str(e)}"


def remove_item(name):
    """
    Removes an item from the inventory.

    Parameters:
    - name (str): The name of the item to be removed.

    Returns:
    - A tuple (success, result):
      - success (bool): True if the item was removed successfully, False if an error occurred.
      - result (dict or str): A dictionary containing the item's name if successful,
                              or an error message if there was an issue.
    """
    try:
        item = Inventory.query.filter_by(name=name).first()
        if not item:
            return False, "Item not found"

        db.session.delete(item)
        db.session.commit()
        return True, {"name": name}
    except Exception as e:
        return False, f"Error removing item: {str(e)}"


def update_quantity(name, quantity):
    """
    Updates the quantity of an existing item in the inventory.

    Parameters:
    - name (str): The name of the item whose quantity is to be updated.
    - quantity (int): The new quantity to set for the item.

    Returns:
    - A tuple (success, result):
      - success (bool): True if the quantity was updated successfully, False if an error occurred.
      - result (dict or str): A dictionary containing the item's name and updated quantity if successful,
                              or an error message if there was an issue.
    """
    try:
        if not isinstance(quantity, int):
            return False, "Quantity must be an integer"

        item = Inventory.query.filter_by(name=name).first()
        if not item:
            return False, "Item not found"

        item.quantity = quantity
        db.session.commit()
        return True, {"name": name, "quantity": quantity}
    except Exception as e:
        return False, f"Error updating quantity: {str(e)}"
