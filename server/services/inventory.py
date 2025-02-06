from database import db
from models.inventory import Inventory

def get_items():
    try:
        items = Inventory.query.all()

        items_list = [{"name": item.name, "quantity": item.quantity} for item in items]

        return True, items_list if items_list else []
    except Exception as e:
        return False, f"Error getting items: {str(e)}"


def add_item(name, quantity):
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
