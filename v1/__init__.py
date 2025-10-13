from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import models so they’re registered
    from . import models  

    # Create tables
    with app.app_context():
        db.create_all()

    # Register routes
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
