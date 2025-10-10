import jwt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.book_routes import book_bp
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(book_bp, url_prefix="/api/books")  # REST API
    app.register_blueprint(auth_bp)  # HTML routes

    with app.app_context():
        db.create_all()

    return app
