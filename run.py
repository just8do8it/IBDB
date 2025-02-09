from app import app, db
import os

if __name__ == "__main__":
    with app.app_context():
        if not os.path.exists("database.db"):
            db.create_all()
            print("Database created!")

    app.run(debug=True)
