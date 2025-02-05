from flask import Blueprint, request
from services.inventory import add_item, remove_item, update_quantity
from utils.responses import success_response, error_response
from utils.delayed_response import delayed_response
import logging

inventory_bp = Blueprint("inventory", __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@inventory_bp.route('/add-item', methods=['POST'])
def add_item_route():
    try:
        data = request.json
        name, quantity = data.get("name"), data.get("quantity")
        logger.info(f"Received request at /add-item with data: {data}")
    except Exception as e:
        return delayed_response(error_response(f"Invalid JSON: {str(e)}"))

    if not name or quantity is None:
        return delayed_response(error_response("Missing name or quantity"))

    success, result = add_item(name, quantity)
    return delayed_response(success_response("Item added successfully", result) if success else error_response(result))

@inventory_bp.route('/remove-item', methods=['DELETE'])
def remove_item_route():
    try:
        data = request.json
        name = data.get("name")
        logger.info(f"Received request at /remove-item with data: {data}")
    except Exception as e:
        return delayed_response(error_response(f"Invalid JSON: {str(e)}"))

    if not name:
        return delayed_response(error_response("Missing name"))

    success, result = remove_item(name)
    return delayed_response(success_response("Item removed successfully", result) if success else error_response(result, 404))

@inventory_bp.route('/update-quantity', methods=['PUT'])
def update_quantity_route():
    try:
        data = request.json
        name, quantity = data.get("name"), data.get("quantity")
        logger.info(f"Received request at /update-quantity with data: {data}")
    except Exception as e:
        return delayed_response(error_response(f"Invalid JSON: {str(e)}"))

    if not name or quantity is None:
        return delayed_response(error_response("Missing name or quantity"))

    success, result = update_quantity(name, quantity)
    return delayed_response(success_response("Quantity updated successfully", result) if success else error_response(result, 404))
