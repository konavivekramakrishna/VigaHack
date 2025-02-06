from flask import Flask
from config import Config
from database import db, init_app
from routes import register_blueprints

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration

init_app(app)  # Initialize database

register_blueprints(app)  # Register route blueprints

if __name__ == "__main__":
    app.run()  # Run the Flask app
