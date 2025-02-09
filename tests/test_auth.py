from app import app, db, bcrypt
from app.models import User
from flask_login import login_user, logout_user, current_user

def test_register(test_client):
    with app.app_context():
        existing_user = User.query.filter_by(email="newuser@example.com").first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()

    response = test_client.post("/register", data={
        "email": "newuser@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    with app.app_context():
        assert User.query.filter_by(email="newuser@example.com").first() is not None

def test_login(test_client, new_user):
    response = test_client.post("/login", data={
        "email": "testuser@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    with test_client.session_transaction() as session:
        assert session["_user_id"] is not None

def test_logout(test_client, new_user):
    test_client.post("/login", data={
        "email": "testuser@example.com",
        "password": "password123"
    }, follow_redirects=True)

    response = test_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    with test_client.session_transaction() as session:
        assert "_user_id" not in session
