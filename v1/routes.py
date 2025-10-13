from flask import Blueprint, jsonify, request
from .models import db, Book

bp = Blueprint('routes', __name__)

@bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([b.to_dict() for b in books])

@bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    return jsonify(book.to_dict())

@bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

@bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    db.session.commit()
    return jsonify(book.to_dict())

@bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})

@bp.route('/books/<int:book_id>/borrow', methods=['POST'])
def borrow_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    if book.state == 'borrowed':
        return jsonify({"message": "Book already borrowed"}), 400
    book.state = 'borrowed'
    db.session.commit()
    return jsonify({"message": "Book borrowed", "book": book.to_dict()})

@bp.route('/books/<int:book_id>/return', methods=['POST'])
def return_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    if book.state == 'available':
        return jsonify({"message": "Book is not borrowed"}), 400
    book.state = 'available'
    db.session.commit()
    return jsonify({"message": "Book returned", "book": book.to_dict()})