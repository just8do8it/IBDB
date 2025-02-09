**📖 IBDB - Internet Book Database**  
*A Flask-based platform for finding, saving, and downloading PDF books.*

---

**🌟 Features**
- 📚 **Book Search**: Search by title, author, description, tags, genre, language, and year.
- 🎯 **Advanced Filtering**: Filter by rating, number of downloads, genre, language, and more.
- 🔝 **Sorting Options**: Sort results by name, year, rating, and downloads in ascending or descending order.
- ⭐ **Favorites**: Save books to a personal favorites list.
- 📂 **Collections**: Create, edit, and share personal book lists.
- ✍️ **Book Reviews**: Users can review books and ratings are dynamically updated.
- 📩 **Download Books**: Download books directly to your machine.
- 🔒 **User Authentication**: Secure login & registration.
- 📧 **Email Delivery**: (Optional) Send books to an email.
- 🛠 **Admin Panel**: Manage books, users, and collections.
- 📊 **Test Coverage > 99%**: Comprehensive automated tests.

---

**🚀 Technologies Used**
| Tech | Purpose |
|------|---------|
| **Flask** | Web framework |
| **Flask-SQLAlchemy** | Database ORM |
| **Flask-Login** | Authentication |
| **Flask-WTF** | Form handling |
| **Flask-Mail** | Email functionality |
| **SQLite** | Database |
| **bcrypt** | Password hashing |
| **pytest** | Automated testing |
| **coverage** | Test coverage analysis |

---

**📥 Installation**
1️⃣ **Clone the Repository**
```sh
git clone https://github.com/yourusername/IBDB.git
cd IBDB
```

2️⃣ **Create a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate      # For Windows
```

3️⃣ **Install Dependencies**
```sh
pip install -r requirements.txt
```

4️⃣ **Set Up the Database**
```sh
flask db upgrade
```
💡 (If using SQLite, ensure the database file exists and migrations are applied.)

5️⃣ **Run the Application**
```sh
flask run
```
🌎 Visit http://127.0.0.1:5000/ in your browser.



**📂 Project Structure**
```bash
📁 IBDB/
│── 📁 app/
│   ├── __init__.py       # App initialization
│   ├── models.py         # Database models
│   ├── routes.py         # Application routes
│   ├── forms.py          # WTForms for user input
│   ├── email_service.py  # Email sending logic
│   ├── static/           # CSS, JS, images
│   ├── templates/        # HTML files
│── 📁 tests/
│   ├── test_auth.py      # Authentication tests
│   ├── test_books.py     # Book-related tests
│   ├── test_lists.py     # Collections tests
│── .env                  # Environment variables
│── config.py             # Configuration settings
│── run.py                # Application entry point
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
```

**🔑 Authentication**
Users must register and log in to create collections and download books.
Passwords are securely hashed using bcrypt.


**🔍 Searching for Books**
Users can search by keyword (title, author, description, tags).
Filters available:
- ✅ Genre
- ✅ Language
- ✅ Year
- ✅ Rating
- ✅ Number of Downloads


**📂 Managing Book Collections**
Users can create, edit, and delete their own public or private book lists.
Collections can be sorted and filtered by name or date.
Sharing feature: Generate a unique link to share collections.
⭐ Book Reviews & Ratings
Users can rate and review books.
Book ratings update dynamically based on user reviews.

**📥 Downloading Books**
Click "Download" to get the book as a PDF.
Users can choose to send the book via email.


**🛠 Running Tests**

1️⃣ **Run all tests**
```sh
pytest tests/
```

2️⃣ **Check test coverage**
```sh
coverage run -m pytest && coverage report -m
```

3️⃣ **Generate HTML Coverage Report**
```sh
coverage html
```
Open htmlcov/index.html to view the report.


**🎨 UI Design**
Modern, elegant design inspired by luxury interior aesthetics.
Color theme: Dark green, gold accents, and modern gradients.
Fully responsive for desktop & mobile.
Consistent UI across all pages (collections, search, books, profile).

**🚀 Future Features**
- 📌 User-generated book uploads (pending moderation).
- 📌 Book recommendations based on reading history.
- 📌 API for book search & download.
- 📌 Dark mode toggle.
- 📌 OAuth (Google, GitHub) Login.


**👨‍💻 Contributors**
💡 Project Lead: Your Name
💡 Developers: Team Members' Names

**🚀 Want to contribute? Open an issue or submit a pull request!**

**📜 License**
This project is licensed under the MIT License. See LICENSE.md for details.

**🎉 Thank you for using IBDB! Happy Reading! 📚**