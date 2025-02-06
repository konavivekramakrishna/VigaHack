from flask import jsonify
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def success_response(message, data=None, status_code=200):
    response = {
        "message": message,
    }
    if data or data==[]:
        response["data"] = data
    return jsonify(response), status_code

def error_response(message, status_code=400):
    return jsonify({"error": message}), status_code
