from flask import Blueprint, request
from utils.responses import success_response
from utils.delayed_response import delayed_response
import logging

transforms_bp = Blueprint("transforms", __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@transforms_bp.route("/transform", methods=["POST"])
def transform():
    """
    Handles a transformation request with arbitrary data.

    Parameters:
    - data (dict): The JSON data passed in the POST request.

    Returns:
    - A JSON response with a success message and the received data.
    """
    data = request.json
    logger.info(f"Received request at /transform with data: {data}")
    return delayed_response(success_response("Transform received", {"data": data}))


@transforms_bp.route("/translation", methods=["POST"])
def translation():
    """
    Handles a translation request with the position data.

    Parameters:
    - position (dict): The position information passed in the POST request.

    Returns:
    - A JSON response with a success message and the received position.
    """
    position = request.json.get("position")
    logger.info(f"Received request at /translation with position: {position}")
    return delayed_response(
        success_response("Translation received", {"position": position})
    )


@transforms_bp.route("/rotation", methods=["POST"])
def rotation():
    """
    Handles a rotation request with the rotation data.

    Parameters:
    - rotation (dict): The rotation information passed in the POST request.

    Returns:
    - A JSON response with a success message and the received rotation.
    """
    rotation = request.json.get("rotation")
    logger.info(f"Received request at /rotation with rotation: {rotation}")
    return delayed_response(
        success_response("Rotation received", {"rotation": rotation})
    )


@transforms_bp.route("/scale", methods=["POST"])
def scale():
    """
    Handles a scale request with the scale data.

    Parameters:
    - scale (dict): The scale information passed in the POST request.

    Returns:
    - A JSON response with a success message and the received scale.
    """
    scale = request.json.get("scale")
    logger.info(f"Received request at /scale with scale: {scale}")
    return delayed_response(success_response("Scale received", {"scale": scale}))
