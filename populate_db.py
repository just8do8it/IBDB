import os
import random
from faker import Faker
from app import app, db
from app.models import *

fake = Faker()

GENRES = ["Science Fiction", "Fantasy", "Mystery", "Romance", "Horror", "Biography", "History", "Philosophy", "Poetry"]
LANGUAGES = ["English", "Bulgarian", "French", "German", "Spanish", "Italian"]

BOOK_FOLDER = "static/books/"

def populate_users_and_lists():
    with app.app_context():

        users = []
        for _ in range(5):  
            email = fake.email()
            password = fake.password(length=10)  
            user = User(email=email, password=password)
            db.session.add(user)
            users.append(user)

        db.session.commit()  


        books = Book.query.all()
        book_count = len(books)
        
        if book_count == 0:
            print("No books found in the database! Add books before running this script.")
            return


        for user in users:
            for _ in range(3):  
                list_name = fake.sentence(nb_words=3)
                is_public = random.choice([True, False])  
                
                book_list = BookList(name=list_name, user_id=user.id, is_public=is_public)
                db.session.add(book_list)
                

                selected_books = random.sample(books, min(10, book_count))  
                book_list.books.extend(selected_books)

        db.session.commit()
        print("✅ Users and book lists successfully populated!")


def assign_collections_to_users():
    with app.app_context():
        users = User.query.all()
        books = Book.query.all()

        if not users or not books:
            print("No users or books found! Ensure you have users and books in the database before running this script.")
            return

        for user in users:
            for _ in range(5):  
                list_name = f"{user.email.split('@')[0]}'s Collection {_+1}"
                is_public = random.choice([True, False])  

                book_list = BookList(name=list_name, user_id=user.id, is_public=is_public)
                db.session.add(book_list)
                db.session.commit()  


                selected_books = random.sample(books, min(10, len(books)))  
                book_list.books.extend(selected_books)

        db.session.commit()
        print("✅ Successfully assigned 5 collections to every user!")



def add_books_to_db():
    with app.app_context():
        pdf_files = [f for f in os.listdir(BOOK_FOLDER) if f.endswith(".pdf")]

        if not pdf_files:
            print("No PDF files found in the folder!")
            return

        print(f"Found {len(pdf_files)} PDF files. Populating database...")

        for i, pdf in enumerate(pdf_files[:1588]):
            book = Book(
                title=fake.sentence(nb_words=3),
                author=fake.name(),
                description=fake.paragraph(nb_sentences=5),
                rating=None,
                tags=", ".join(fake.words(nb=4)),
                genre=random.choice(GENRES),
                year=random.randint(1800, 2024),
                language=random.choice(LANGUAGES),
                downloads=random.randint(0, 10000),
                file_path=f"{BOOK_FOLDER}{pdf}"
            )

            db.session.add(book)

            if (i + 1) % 100 == 0:
                db.session.commit()
                print(f"{i + 1} books inserted...")

        db.session.commit()
        print("Database successfully populated with 1,588 books!")

def update_book_ratings():
    with app.app_context():
        books = Book.query.all()

        for book in books:
            reviews = Review.query.filter_by(book_id=book.id).all()
            if reviews:
                avg_rating = round(sum(review.rating for review in reviews) / len(reviews), 1)
                book.rating = avg_rating
            else:
                book.rating = None

        db.session.commit()
        print("✅ Successfully updated book ratings based on reviews!")

def populate_reviews():
    with app.app_context():
        users = User.query.all()
        books = Book.query.all()

        if not users or not books:
            print("No users or books found! Ensure you have users and books in the database before running this script.")
            return

        reviews_to_add = []

        for _ in range(50000):  
            user = random.choice(users)
            book = random.choice(books)
            rating = round(random.uniform(1, 5), 1)  
            comment = fake.paragraph(nb_sentences=random.randint(2, 5))  

            review = Review(user_id=user.id, book_id=book.id, rating=rating, comment=comment)
            reviews_to_add.append(review)

        db.session.bulk_save_objects(reviews_to_add)
        db.session.commit()
        
        print("✅ Successfully added 500 reviews to the database!")



if __name__ == "__main__":
    assign_collections_to_users()




