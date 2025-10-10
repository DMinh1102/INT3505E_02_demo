from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes.book_routes import book_bp
    from app.routes.ui_routes import ui_bp
    app.register_blueprint(book_bp, url_prefix="/api/books")  # REST API
    app.register_blueprint(ui_bp)  # HTML routes

    with app.app_context():
        db.create_all()

    return app
