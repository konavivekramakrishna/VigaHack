import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the absolute path of the current directory

class Config:
    # Configure the database URI for SQLite, using a file called 'database.db' in the base directory
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
    # Disable tracking modifications to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
