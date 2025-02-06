from flask import Blueprint, request
from utils.responses import success_response

file_bp = Blueprint("file", __name__)

@file_bp.route('/file-path', methods=['GET'])
def file_path():
    """
    Retrieves the file path based on the query parameter 'projectpath'.
    
    Parameters:
    - projectpath (query parameter): A boolean value passed as a query parameter in the GET request to determine 
      if the file path should point to a project folder ('true') or a DCC file ('false').
    
    Returns:
    - A JSON response containing a success message and the corresponding file path.
    """
    projectpath = request.args.get("projectpath", "false").lower() == "true"
    path = "/path/to/project/folder" if projectpath else "/path/to/dcc/file"
    return success_response("File path retrieved", {"file_path": path})
