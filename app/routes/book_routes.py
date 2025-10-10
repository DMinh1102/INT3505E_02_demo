from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.models import db, Book

book_bp = Blueprint("book_bp", __name__)



# Lấy tất cả sách
@book_bp.route("/", methods=["GET"])
@jwt_required()
def get_books():
    books = Book.query.all()
    return jsonify([{"id": b.id, "title": b.title, "author": b.author, "available": b.available} for b in books])

# Lấy thông tin 1 sách theo id
@book_bp.route("/<int:id>", methods=["GET"])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book.to_dict()), 200

@book_bp.route("/", methods=["POST"])
@jwt_required()
def add_book():
    data = request.get_json()
    title = data["title"] , author = data["author"]
    if not title or not author:
        return jsonify({"error": "Missing title or author"}), 400

    new_book = Book(title=data["title"], author=data["author"])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added"}), 201



# Cập nhật thông tin sách
@book_bp.route("/<int:id>", methods=["PUT"])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    book.available = data.get("available", book.available)
    db.session.commit()
    return jsonify(book.to_dict()), 200

# Xóa sách
@book_bp.route("/<int:id>", methods=["DELETE"])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}), 200
