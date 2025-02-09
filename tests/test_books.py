from app import app, db
from app.models import Book

def test_book_page(test_client):
    with app.app_context():
        new_book = Book(
            title="Test Book",
            author="Test Author",
            description="This is a test book.",  
            file_path="static/books/test.pdf",
            genre="Science Fiction",
            language="English",
            year=2022,
            rating=4.5,
            downloads=10
        )
        db.session.add(new_book)
        db.session.commit()
        book_id = new_book.id

    with app.app_context():
        book = Book.query.get(book_id)
        assert book is not None

    response = test_client.get(f"/book/{book_id}")
    assert response.status_code == 200
    assert b"Test Book" in response.data
