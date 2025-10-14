from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Book, Loan

bp = Blueprint('routes', __name__)

@bp.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    books = Book.query.all()
    return jsonify([b.to_dict() for b in books])

@bp.route('/books/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    return jsonify(book.to_dict())

@bp.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

@bp.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required()
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
@jwt_required()
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})

# List all loans
@bp.route('/loans', methods=['GET'])
@jwt_required()
def get_loans():
    loans = Loan.query.all()
    return jsonify([l.to_dict() for l in loans])

# Borrow (create a loan)
@bp.route('/loans', methods=['POST'])
@jwt_required()
def borrow_book():
    data = request.get_json()
    book_id = data.get('book_id')
    borrower_name = data.get('borrower_name')

    if not book_id or not borrower_name:
        return jsonify({"message": "book_id and borrower_name are required"}), 400

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    if book.is_borrowed:
        return jsonify({"message": "Book already borrowed"}), 400

    loan = Loan(book_id=book_id, borrower_name=borrower_name)
    book.is_borrowed = True

    db.session.add(loan)
    db.session.commit()

    return jsonify(loan.to_dict()), 201

# Return (delete a loan)
@bp.route('/loans/<int:loan_id>', methods=['DELETE'])
@jwt_required()
def return_book(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"message": "Loan not found"}), 404

    book = Book.query.get(loan.book_id)
    book.is_borrowed = False

    db.session.delete(loan)
    db.session.commit()
    return jsonify({"message": f"Book '{book.title}' returned successfully"})