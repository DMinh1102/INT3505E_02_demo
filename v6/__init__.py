from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from .swagger_config import template
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'  
    app.config['SWAGGER'] = {
        'title': 'Library API',
        'uiversion': 3,
        'openapi': '3.0.2'
    }

    db.init_app(app)
    jwt = JWTManager(app)
    swagger = Swagger(app, template= template)

    # Create tables
    from . import models
    with app.app_context():
        db.create_all()

    # Register routes
    from .routes import bp as routes_bp
    from .auth import auth_bp
    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)

    return app
