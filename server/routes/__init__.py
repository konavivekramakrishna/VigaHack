from flask import Blueprint

# Initialize Blueprint (empty for now)
routes_bp = Blueprint("routes", __name__)

# Lazy import to avoid circular imports
def register_blueprints(app):
    from routes.inventory import inventory_bp
    from routes.file import file_bp
    from routes.transforms import transforms_bp

    app.register_blueprint(inventory_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(transforms_bp)
