import time
from flask import jsonify

def delayed_response(response):
    time.sleep(10)
    return response
