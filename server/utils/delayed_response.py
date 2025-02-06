import time
from flask import jsonify

def delayed_response(response):
    """
    Simulates a delay before returning the given response.
    
    Parameters:
    - response (dict or Flask Response): The response to be returned after the delay.
    
    Returns:
    - The same response passed to the function, after a 10-second delay.
    """
    time.sleep(10)  # Introduces a 10-second delay
    return response  # Returns the response after the delay
