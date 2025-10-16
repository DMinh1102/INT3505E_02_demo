from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Book, Loan

bp = Blueprint('routes', __name__)

@bp.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    """
    Get all books
    ---
    tags:
      - Books
    security:
      - Bearer: []
    responses:
      200:
        description: List of all books
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              author:
                type: string
              is_borrowed:
                type: boolean
        examples:
          application/json:
            - id: 1
              title: "The Hobbit"
              author: "J.R.R. Tolkien"
              is_borrowed: false
    """
    books = Book.query.all()
    data = [b.to_dict() for b in books]

    response = make_response(jsonify(data), 200)
    response.headers['Cache-Control'] = 'public, max-age=60'
    response.headers['ETag'] = str(hash(str(data)))
    return response


@bp.route('/books/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):
    """
    Get a single book by ID
    ---
    tags:
      - Books
    security:
      - Bearer: []
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: The ID of the book to retrieve
    responses:
      200:
        description: The requested book
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            author:
              type: string
            is_borrowed:
              type: boolean
      404:
        description: Book not found
    """
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    return jsonify(book.to_dict())


@bp.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    """
    Add a new book
    ---
    tags:
      - Books
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - title
            - author
          properties:
            title:
              type: string
            author:
              type: string
    responses:
      201:
        description: Book successfully created
      400:
        description: Invalid input
    """
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201


@bp.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    """
    Update a book by ID
    ---
    tags:
      - Books
    security:
      - Bearer: []
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID of the book to update
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
    responses:
      200:
        description: Book successfully updated
      404:
        description: Book not found
    """
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
    """
    Delete a book by ID
    ---
    tags:
      - Books
    security:
      - Bearer: []
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID of the book to delete
    responses:
      200:
        description: Book successfully deleted
      404:
        description: Book not found
    """
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})


@bp.route('/loans', methods=['GET'])
@jwt_required()
def get_loans():
    """
    Get all loan records
    ---
    tags:
      - Loans
    security:
      - Bearer: []
    responses:
      200:
        description: List of all loan records
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              book_id:
                type: integer
              borrower_name:
                type: string
              borrow_date:
                type: string
                format: date-time
        examples:
          application/json:
            - id: 1
              book_id: 2
              borrower_name: "Alice"
              borrow_date: "2025-10-13T09:00:00"
    """
    loans = Loan.query.all()
    return jsonify([l.to_dict() for l in loans])


@bp.route('/loans', methods=['POST'])
@jwt_required()
def borrow_book():
    """
    Borrow a book (create a loan)
    ---
    tags:
      - Loans
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - book_id
            - borrower_name
          properties:
            book_id:
              type: integer
            borrower_name:
              type: string
    responses:
      201:
        description: Loan created successfully
      400:
        description: Book already borrowed or invalid input
      404:
        description: Book not found
    """
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


@bp.route('/loans/<int:loan_id>', methods=['DELETE'])
@jwt_required()
def return_book(loan_id):
    """
    Return a borrowed book (delete a loan)
    ---
    tags:
      - Loans
    security:
      - Bearer: []
    parameters:
      - name: loan_id
        in: path
        type: integer
        required: true
        description: ID of the loan record
    responses:
      200:
        description: Book returned successfully
      404:
        description: Loan not found
    """
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"message": "Loan not found"}), 404

    book = Book.query.get(loan.book_id)
    book.is_borrowed = False

    db.session.delete(loan)
    db.session.commit()
    return jsonify({"message": f"Book '{book.title}' returned successfully"})
