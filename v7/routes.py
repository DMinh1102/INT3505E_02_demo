from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import jwt_required
from mongoengine import Q
from .models import Book, Loan
import math

bp = Blueprint('routes', __name__)


@bp.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    """
    Get books with search, filtering and pagination
    ---
    tags:
      - Books
    security:
      - BearerAuth: []
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Page number for pagination
      - name: per_page
        in: query
        type: integer
        required: false
        default: 10
        description: Number of items per page (max 100)
      - name: search
        in: query
        type: string
        required: false
        description: Search term for title or author (case-insensitive)
      - name: author
        in: query
        type: string
        required: false
        description: Filter by specific author
      - name: is_borrowed
        in: query
        type: boolean
        required: false
        description: Filter by borrowed status (true/false)
      - name: sort_by
        in: query
        type: string
        required: false
        default: title
        enum: [title, author, id, created_at]
        description: Field to sort by
      - name: sort_order
        in: query
        type: string
        required: false
        default: asc
        enum: [asc, desc]
        description: Sort order
    responses:
      200:
        description: Paginated list of books with metadata
        content:
          application/json:
            schema:
              type: object
              properties:
                books:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                      title:
                        type: string
                      author:
                        type: string
                      is_borrowed:
                        type: boolean
                      created_at:
                        type: string
                        format: date-time
                pagination:
                  type: object
                  properties:
                    page:
                      type: integer
                    per_page:
                      type: integer
                    total_pages:
                      type: integer
                    total_items:
                      type: integer
                    has_next:
                      type: boolean
                    has_prev:
                      type: boolean
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '').strip()
    author_filter = request.args.get('author', '').strip()
    is_borrowed_filter = request.args.get('is_borrowed', type=lambda x: x.lower() == 'true' if x else None)
    sort_by = request.args.get('sort_by', 'title')
    sort_order = request.args.get('sort_order', 'asc')

    # Validate
    if page < 1:
        return jsonify({"error": "Page must be greater than 0"}), 400
    if per_page < 1 or per_page > 100:
        return jsonify({"error": "per_page must be between 1 and 100"}), 400

    valid_sort_fields = ['title', 'author', 'id', 'created_at']
    if sort_by not in valid_sort_fields:
        return jsonify({"error": f"Invalid sort field. Must be one of: {', '.join(valid_sort_fields)}"}), 400

    # Build query
    query = Q()
    if search:
        query &= Q(title__icontains=search) | Q(author__icontains=search)
    if author_filter:
        query &= Q(author__icontains=author_filter)
    if is_borrowed_filter is not None:
        query &= Q(is_borrowed=is_borrowed_filter)

    # Sort
    order_prefix = '-' if sort_order == 'desc' else ''
    order_field = order_prefix + sort_by

    total_items = Book.objects(query).count()
    total_pages = math.ceil(total_items / per_page)
    books = (
        Book.objects(query)
        .order_by(order_field)
        .skip((page - 1) * per_page)
        .limit(per_page)
    )

    response_data = {
        "books": [b.to_dict() for b in books],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }

    response = make_response(jsonify(response_data), 200)
    response.headers['Cache-Control'] = 'public, max-age=60'
    return response



@bp.route('/books/<string:book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):
    """
    Get a single book by ID
    ---
    tags:
      - Books
    security:
      - BearerAuth: []
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
        description: The ID of the book to retrieve
    responses:
      200:
        description: The requested book
      404:
        description: Book not found
    """
    book = Book.objects(id=book_id).first()
    if not book:
        return jsonify({"message": "Book not found"}), 404
    return jsonify(book.to_dict())


# ---------------------------
# 📘 POST /books
# ---------------------------
@bp.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    """
    Add a new book
    ---
    tags:
      - Books
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
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
    if not data.get('title') or not data.get('author'):
        return jsonify({"error": "Missing required fields"}), 400
    book = Book(title=data['title'], author=data['author']).save()
    return jsonify(book.to_dict()), 201



@bp.route('/books/<string:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    """
    Update a book by ID
    ---
    tags:
      - Books
    security:
      - BearerAuth: []
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
        description: ID of the book to update
    responses:
      200:
        description: Book successfully updated
      404:
        description: Book not found
    """
    book = Book.objects(id=book_id).first()
    if not book:
        return jsonify({"message": "Book not found"}), 404
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.save()
    return jsonify(book.to_dict())


@bp.route('/books/<string:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    """
    Delete a book by ID
    ---
    tags:
      - Books
    security:
      - BearerAuth: []
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
        description: ID of the book to delete
    responses:
      200:
        description: Book successfully deleted
      404:
        description: Book not found
    """
    book = Book.objects(id=book_id).first()
    if not book:
        return jsonify({"message": "Book not found"}), 404
    book.delete()
    return jsonify({"message": "Book deleted"})


# ---------------------------
# 📘 GET /loans
# ---------------------------
@bp.route('/loans', methods=['GET'])
@jwt_required()
def get_loans():
    """
    Get all loan records
    ---
    tags:
      - Loans
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of all loan records
    """
    loans = Loan.objects()
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
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - book_id
              - borrower_name
            properties:
              book_id:
                type: string
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

    book = Book.objects(id=book_id).first()
    if not book:
        return jsonify({"message": "Book not found"}), 404
    if book.is_borrowed:
        return jsonify({"message": "Book already borrowed"}), 400

    loan = Loan(book=book, borrower_name=borrower_name).save()
    book.is_borrowed = True
    book.save()

    return jsonify(loan.to_dict()), 201



@bp.route('/loans/<string:loan_id>', methods=['DELETE'])
@jwt_required()
def return_book(loan_id):
    """
    Return a borrowed book (delete a loan)
    ---
    tags:
      - Loans
    security:
      - BearerAuth: []
    parameters:
      - name: loan_id
        in: path
        type: string
        required: true
        description: ID of the loan record
    responses:
      200:
        description: Book returned successfully
      404:
        description: Loan not found
    """
    loan = Loan.objects(id=loan_id).first()
    if not loan:
        return jsonify({"message": "Loan not found"}), 404

    book = loan.book
    if book:
        book.is_borrowed = False
        book.save()

    loan.delete()
    return jsonify({"message": f"Book '{book.title}' returned successfully"})
