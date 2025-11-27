from datetime import datetime
from mongoengine import Document, StringField, BooleanField, DateTimeField, ReferenceField
from flask_bcrypt import generate_password_hash, check_password_hash

# ----- Book model -----
class Book(Document):
    meta = {"collection": "books"}  # tương đương __tablename__
    
    title = StringField(required=True, max_length=100)
    author = StringField(required=True, max_length=100)
    is_borrowed = BooleanField(default=False)

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "author": self.author,
            "is_borrowed": self.is_borrowed
        }


# ----- Loan model -----
class Loan(Document):
    meta = {"collection": "loans"}
    
    book = ReferenceField(Book, required=True, reverse_delete_rule=2)  # CASCADE delete
    borrower_name = StringField(required=True, max_length=100)
    borrowed_at = DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "book_id": str(self.book.id) if self.book else None,
            "borrower_name": self.borrower_name,
            "borrowed_at": self.borrowed_at.isoformat()
        }


# ----- User model -----
class User(Document):
    meta = {"collection": "users"}

    username = StringField(required=True, unique=True, max_length=80)
    password_hash = StringField(required=True, max_length=200)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
