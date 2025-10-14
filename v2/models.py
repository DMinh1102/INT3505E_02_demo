from datetime import datetime
from . import db

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_borrowed = db.Column(db.Boolean, default=False)
    
    loan = db.relationship('Loan', backref='book', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "is_borrowed": self.is_borrowed
        }

class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrower_name = db.Column(db.String(100), nullable=False)
    borrowed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "borrower_name": self.borrower_name,
            "borrowed_at": self.borrowed_at.isoformat()
        }
