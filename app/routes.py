from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Book

main = Blueprint("main", __name__)

@main.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html", books=books)

@main.route("/add", methods=["POST"])
def add_book():
    title = request.form["title"]
    author = request.form["author"]
    new_book = Book(title=title, author=author)
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for("main.index"))

@main.route("/borrow/<int:id>")
def borrow_book(id):
    book = Book.query.get(id)
    if book and book.available:
        book.available = False
        db.session.commit()
    return redirect(url_for("main.index"))

@main.route("/return/<int:id>")
def return_book(id):
    book = Book.query.get(id)
    if book and not book.available:
        book.available = True
        db.session.commit()
    return redirect(url_for("main.index"))
