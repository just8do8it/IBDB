import pytest
from app import app, db, bcrypt
from app.models import User
from flask_login import login_user
from werkzeug.security import generate_password_hash

@pytest.fixture(scope="module")
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def new_user():
    with app.app_context():
        existing_user = User.query.filter_by(email="testuser@example.com").first()
        if not existing_user:
            user = User(email="testuser@example.com", password=bcrypt.generate_password_hash("password123").decode("utf-8"))
            db.session.add(user)
            db.session.commit()
        return User.query.filter_by(email="testuser@example.com").first()
