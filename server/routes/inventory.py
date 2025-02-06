from flask import Blueprint, request, jsonify
from services.inventory import add_item, remove_item, update_quantity, get_items
from utils.responses import success_response, error_response
from utils.delayed_response import delayed_response
import logging

inventory_bp = Blueprint("inventory", __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@inventory_bp.route("/add-item", methods=["POST"])
def add_item_route():
    """
    Adds an item to the inventory.
    
    Parameters:
    - name (str): The name of the item to be added.
    - quantity (int): The quantity of the item to be added.
    
    Returns:
    - A JSON response with a success message if the item was added or an error message if there was an issue.
    """
    try:
        data = request.json
        name, quantity = data.get("name"), data.get("quantity")
        logger.info(f"Received request at /add-item with data: {data}")
    except Exception as e:
        return delayed_response(error_response(f"Invalid JSON: {str(e)}"))

    if not name or quantity is None:
        return delayed_response(error_response("Missing name or quantity"))

    if not isinstance(quantity, int):
        return delayed_response(error_response("Quantity must be an integer"))

    success, result = add_item(name, quantity)
    return delayed_response(
        success_response("Item added successfully", result, 201)
        if success
        else error_response(result)
    )


@inventory_bp.route("/remove-item", methods=["DELETE"])
def remove_item_route():
    """
    Removes an item from the inventory.
    
    Parameters:
    - name (str): The name of the item to be removed.
    
    Returns:
    - A JSON response with a success message if the item was removed or an error message if there was an issue.
    """
    try:
        data = request.json
        name = data.get("name")
        logger.info(f"Received request at /remove-item with data: {data}")
    except Exception as e:
        return delayed_response(error_response(f"Invalid JSON: {str(e)}"))

    if not name:
        return delayed_response(error_response("Missing name"))

    success, result = remove_item(name)
    return delayed_response(
        success_response("Item removed successfully", result)
        if success
        else error_response(result, 404)
    )


@inventory_bp.route("/update-quantity", methods=["PUT"])
def update_quantity_route():
    """
    Updates the quantity of an existing item in the inventory.
    
    Parameters:
    - name (str): The name of the item whose quantity is to be updated.
    - quantity (int): The new quantity to be set for the item.
    
    Returns:
    - A JSON response with a success message if the quantity was updated or an error message if there was an issue.
    """
    try:
        data = request.json
        name, quantity = data.get("name"), data.get("quantity")
        logger.info(f"Received request at /update-quantity with data: {data}")
    except Exception as e:
        return delayed_response(error_response(f"Invalid JSON: {str(e)}"))

    if not name or quantity is None:
        return delayed_response(error_response("Missing name or quantity"))

    if not isinstance(quantity, int):
        return delayed_response(error_response("Quantity must be an integer"))

    success, result = update_quantity(name, quantity)
    return delayed_response(
        success_response("Quantity updated successfully", result)
        if success
        else error_response(result, 404)
    )


@inventory_bp.route("/get-items", methods=["GET"])
def get_items_route():
    """
    Retrieves all the items in the inventory.
    
    Parameters:
    - None.
    
    Returns:
    - A JSON response containing a list of items if successful or an error message if there was an issue.
    """
    success, result = get_items()
    return delayed_response(
        success_response("Items retrieved successfully", result)
        if success
        else error_response(result, 404)
    )
