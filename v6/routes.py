from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Book, Loan

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
                        type: integer
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
            examples:
              application/json:
                books:
                  - id: 1
                    title: "The Hobbit"
                    author: "J.R.R. Tolkien"
                    is_borrowed: false
                    created_at: "2024-01-15T10:30:00"
                pagination:
                  page: 1
                  per_page: 10
                  total_pages: 5
                  total_items: 48
                  has_next: true
                  has_prev: false
      400:
        description: Invalid pagination or filter parameters
    """
    # Get query parameters with defaults
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '').strip()
    author_filter = request.args.get('author', '').strip()
    is_borrowed_filter = request.args.get('is_borrowed', type=lambda x: x.lower() == 'true' if x else None)
    sort_by = request.args.get('sort_by', 'title')
    sort_order = request.args.get('sort_order', 'asc')

    # Validate pagination parameters
    if page < 1:
        return jsonify({"error": "Page must be greater than 0"}), 400
    if per_page < 1 or per_page > 100:
        return jsonify({"error": "per_page must be between 1 and 100"}), 400

    # Validate sort parameters
    valid_sort_fields = ['title', 'author', 'id', 'created_at']
    if sort_by not in valid_sort_fields:
        return jsonify({"error": f"Invalid sort field. Must be one of: {', '.join(valid_sort_fields)}"}), 400

    # Start building query
    query = Book.query

    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Book.title.ilike(search_term),
                Book.author.ilike(search_term)
            )
        )

    # Apply author filter
    if author_filter:
        query = query.filter(Book.author.ilike(f"%{author_filter}%"))

    # Apply borrowed status filter
    if is_borrowed_filter is not None:
        query = query.filter(Book.is_borrowed == is_borrowed_filter)

    # Apply sorting
    sort_column = getattr(Book, sort_by)
    if sort_order == 'desc':
        sort_column = sort_column.desc()
    query = query.order_by(sort_column)

    # Execute paginated query
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    # Prepare response data
    books_data = [book.to_dict() for book in pagination.items]

    response_data = {
        "books": books_data,
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_pages": pagination.pages,
            "total_items": pagination.total,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    }

    # Add caching headers
    response = make_response(jsonify(response_data), 200)
    response.headers['Cache-Control'] = 'public, max-age=60'
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
      - BearerAuth: []
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
                example: "The Great Gatsby"
              author:
                type: string
                example: "F. Scott Fitzgerald"
    responses:
      201:
        description: Book successfully created
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                title:
                  type: string
                  example: "The Great Gatsby"
                author:
                  type: string
                  example: "F. Scott Fitzgerald"
                created_at:
                  type: string
                  format: date-time
      400:
        description: Invalid input
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Missing required fields"
      401:
        $ref: '#/components/responses/Unauthorized'
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
      - BearerAuth: []
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
      - BearerAuth: []
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
      - BearerAuth: []
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
      - BearerAuth: []
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
      - BearerAuth: []
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
