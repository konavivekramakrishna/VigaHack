from flask import jsonify

def success_response(message, data=None):
    response = {"message": message}
    if data:
        response.update(data)
    return jsonify(response), 200

def error_response(message, status_code=400):
    return jsonify({"error": message}), status_code
