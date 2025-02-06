from flask import jsonify
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def success_response(message, data=None, status_code=200):
    """
    Creates a success response with a message and optional data.
    
    Parameters:
    - message (str): The success message.
    - data (any): Optional data to include in the response.
    - status_code (int): HTTP status code (default 200).
    
    Returns:
    - JSON response and status code.
    """
    response = {"message": message}
    if data or data==[]:
        response["data"] = data
    return jsonify(response), status_code

def error_response(message, status_code=400):
    """
    Creates an error response with a message.
    
    Parameters:
    - message (str): The error message.
    - status_code (int): HTTP status code (default 400).
    
    Returns:
    - JSON error response and status code.
    """
    return jsonify({"error": message}), status_code
