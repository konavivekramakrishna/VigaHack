from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy instance

def init_app(app):
    db.init_app(app)  # Initialize the app with SQLAlchemy
    with app.app_context():
        from models import inventory  # Import the models
        db.create_all()  # Create all database tables based on the models
