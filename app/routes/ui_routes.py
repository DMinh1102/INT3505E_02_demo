from flask import Blueprint, render_template
from app.models import Book

ui_bp = Blueprint("ui_bp", __name__)

@ui_bp.route("/")
def home():
    books = Book.query.all()
    return render_template("index.html", books=books)
