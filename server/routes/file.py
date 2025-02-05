from flask import Blueprint, request
from utils.responses import success_response

file_bp = Blueprint("file", __name__)

@file_bp.route('/file-path', methods=['GET'])
def file_path():
    projectpath = request.args.get("projectpath", "false").lower() == "true"
    path = "/path/to/project/folder" if projectpath else "/path/to/dcc/file"
    return success_response("File path retrieved", {"file_path": path})
