from app import app, db
from app.models import BookList, User

def test_edit_list(test_client, new_user):
    with app.app_context():
        book_list = BookList(name="Editable List", user_id=new_user.id, is_public=True)
        db.session.add(book_list)
        db.session.commit()
        list_id = book_list.id  # Store the ID before leaving the session

    test_client.post("/login", data={"email": "testuser@example.com", "password": "password123"})

    response = test_client.post(f"/edit_list/{list_id}", data={"name": "Updated List", "is_public": "0"}, follow_redirects=True)

    with app.app_context():
        updated_list = BookList.query.get(list_id)
        assert updated_list is not None

    assert response.status_code == 200
    assert updated_list.name == "Updated List"
    assert not updated_list.is_public

def test_delete_list(test_client, new_user):
    with app.app_context():
        book_list = BookList(name="To Delete", user_id=new_user.id, is_public=True)
        db.session.add(book_list)
        db.session.commit()
        list_id = book_list.id

    test_client.post("/login", data={"email": "testuser@example.com", "password": "password123"})

    response = test_client.post(f"/delete_list/{list_id}", follow_redirects=True)

    with app.app_context():
        deleted_list = BookList.query.get(list_id)

    assert response.status_code == 200
    assert deleted_list is None
