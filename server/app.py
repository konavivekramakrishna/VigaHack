from flask import Flask
from config import Config
from database import db, init_app
from routes import register_blueprints

app = Flask(__name__)
app.config.from_object(Config)

init_app(app)

register_blueprints(app)

if __name__ == "__main__":
    app.run(debug=True)
