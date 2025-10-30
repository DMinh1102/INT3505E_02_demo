from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from .swagger_config import template

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'  
    app.config['SWAGGER'] = {
        'title': 'Library API',
        'uiversion': 3,
        'openapi': '3.0.2'
    }
    app.config['MONGODB_SETTINGS'] = {
        'db': 'librarydb',
        'host': 'localhost',
        'port': 27017
    }

    db.init_app(app)
    jwt = JWTManager(app)
    swagger = Swagger(app, template= template)
    

    # Register routes
    from .routes import bp as routes_bp
    from .auth import auth_bp
    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)

    return app
