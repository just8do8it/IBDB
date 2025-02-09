from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import uuid

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    favorites = db.relationship("Book", secondary="favorites", backref="users")
    lists = db.relationship("BookList", backref="user", lazy=True)  

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, default=0.0)
    tags = db.Column(db.String(255))  
    genre = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    downloads = db.Column(db.Integer, default=0)
    file_path = db.Column(db.String(255), nullable=False)

class BookList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    is_public = db.Column(db.Boolean, default=False)  
    share_link = db.Column(db.String(50), unique=True, nullable=True)  
    books = db.relationship("Book", secondary="list_books", backref="book_lists")


    def generate_share_link(self):
        self.share_link = str(uuid.uuid4())[:8]  
        db.session.commit()


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    rating = db.Column(db.Float, nullable=False)  
    comment = db.Column(db.Text, nullable=False)

    user = db.relationship("User", backref=db.backref("reviews", lazy=True))
    book = db.relationship("Book", backref=db.backref("reviews", lazy=True))

list_books = db.Table(
    "list_books",
    db.Column("list_id", db.Integer, db.ForeignKey("book_list.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
)

favorites = db.Table(
    "favorites",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
)
