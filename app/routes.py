from flask import render_template, redirect, url_for, flash, request, send_file
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, bcrypt
from app.models import User, Book, Review, BookList
from app.forms import RegisterForm, LoginForm, ReviewForm, CreateListForm, SearchForm
from app.email_service import send_book_email
from werkzeug.utils import safe_join
import os




@app.route("/")
def index():
    return redirect("/search")





@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)






@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template("login.html", form=form)






@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))






@app.route("/book/<int:book_id>", methods=["GET", "POST"])
def book_page(book_id):
    book = Book.query.get_or_404(book_id)
    form = ReviewForm()

    if form.validate_on_submit():
        new_review = Review(
            user_id=current_user.id,
            book_id=book_id,
            rating=form.rating.data,
            comment=form.comment.data
        )
        db.session.add(new_review)
        db.session.commit()


        reviews = Review.query.filter_by(book_id=book_id).all()
        book.rating = round(sum(r.rating for r in reviews) / len(reviews), 1)
        db.session.commit()

        flash("Review added!", "success")
        return redirect(url_for("book_page", book_id=book.id))

    return render_template("book.html", book=book, form=form)






@app.route("/search", methods=["GET"])
def search():
    form = SearchForm()
    query = request.args.get("q", "")
    books = Book.query


    if query:
        books = books.filter(
            (Book.title.ilike(f"%{query}%")) |
            (Book.author.ilike(f"%{query}%")) |
            (Book.description.ilike(f"%{query}%")) |
            (Book.tags.ilike(f"%{query}%"))
        )


    if request.args.get("year"):
        books = books.filter(Book.year == int(request.args.get("year")))

    if request.args.get("genre"):
        books = books.filter(Book.genre.ilike(f"%{request.args.get('genre')}%"))

    if request.args.get("language"):
        books = books.filter(Book.language == request.args.get("language"))


    sort_by = request.args.get("sort", "title")  
    order = request.args.get("order", "asc")  


    sort_field = {
        "title": Book.title,
        "author": Book.author,
        "year": Book.year,
        "rating": Book.rating,
        "downloads": Book.downloads
    }.get(sort_by, Book.title)


    if order == "desc":
        books = books.order_by(sort_field.desc())
    else:
        books = books.order_by(sort_field.asc())

    books = books.all()
    
    return render_template("search.html", books=books, query=query, form=form, sort_by=sort_by, order=order)
































@app.route("/download/<int:book_id>", methods=["GET", "POST"])
def download_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    if request.method == "POST":
        recipient_email = request.form.get("email")
        send_book_email(recipient_email, book.title, book.file_path)  
        book.downloads += 1
        db.session.commit()
        flash("Book sent to your email!", "success")
        return redirect(url_for("book_page", book_id=book.id))

    return render_template("download.html", book=book)






@app.route("/lists")
@login_required
def lists():
    lists = BookList.query.filter_by(user_id=current_user.id).all()
    return render_template("list.html", lists=lists)






@app.route("/create_list", methods=["GET", "POST"])
@login_required
def create_list():
    form = CreateListForm()
    
    if form.validate_on_submit():
        new_list = BookList(name=form.name.data, user_id=current_user.id, is_public=form.is_public.data)
        db.session.add(new_list)
        db.session.commit()
        flash("Book list created!", "success")
        return redirect(url_for("profile"))

    return render_template("create_list.html", form=form)






@app.route("/list/<int:list_id>")
@login_required
def view_list(list_id):
    book_list = BookList.query.get_or_404(list_id)
    
    if not book_list.is_public and book_list.user_id != current_user.id:
        flash("This list is private.", "danger")
        return redirect(url_for("lists"))

    return render_template("list.html", book_list=book_list)





@app.route("/delete_list/<int:list_id>", methods=["POST"])
@login_required
def delete_list(list_id):
    book_list = BookList.query.get_or_404(list_id)


    if book_list.user_id != current_user.id:
        flash("⚠ You do not have permission to delete this list.", "danger")
        return redirect(url_for("profile"))

    db.session.delete(book_list)
    db.session.commit()
    flash("✅ Book list deleted successfully!", "info")

    return redirect(url_for("profile"))


from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import app, db
from app.models import BookList
from app.forms import CreateListForm




@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = CreateListForm()


    if form.validate_on_submit():
        new_list = BookList(
            name=form.name.data,
            user_id=current_user.id, 
            is_public=form.is_public.data
        )
        db.session.add(new_list)
        db.session.commit()
        flash("✅ Book list created successfully!", "success")
        return redirect(url_for("profile"))  


    user_lists = BookList.query.filter_by(user_id=current_user.id).all()

    return render_template("profile.html", user=current_user, lists=user_lists, form=form)





@app.route("/generate_share_link/<int:list_id>")
@login_required
def generate_share_link(list_id):
    book_list = BookList.query.get_or_404(list_id)


    if book_list.user_id != current_user.id:
        return jsonify({"error": "You do not have permission to share this list."}), 403


    if not book_list.share_link:
        book_list.generate_share_link()
        db.session.commit()


    shareable_url = url_for("shared_list", share_link=book_list.share_link, _external=True)
    return jsonify({"share_link": shareable_url})




@app.route("/public_lists")
@login_required
def public_lists():
    show_my_lists = request.args.get("show_my_lists", "false") == "true"

    if show_my_lists:
        lists = BookList.query.filter_by(user_id=current_user.id).filter_by(is_public=True).all()
    else:
        lists = BookList.query.filter_by(is_public=True).all()

    return render_template("public_lists.html", lists=lists, show_my_lists=show_my_lists)


























@app.route("/edit_list/<int:list_id>", methods=["GET", "POST"])
@login_required
def edit_list(list_id):
    book_list = BookList.query.get_or_404(list_id)


    if book_list.user_id != current_user.id:
        flash("⚠ You do not have permission to edit this list.", "danger")
        return redirect(url_for("profile"))

    form = CreateListForm(obj=book_list)
    selected_books = book_list.books  

    if request.method == "POST":
        book_ids = request.form.getlist("selected_books")  
        selected_books = Book.query.filter(Book.id.in_(book_ids)).all()

        if form.validate_on_submit():
            book_list.name = form.name.data
            book_list.is_public = form.is_public.data


            book_list.books = selected_books
            db.session.commit()

            flash("✅ Book list updated successfully!", "success")
            return redirect(url_for("profile"))


    books = Book.query.all()

    return render_template("edit_list.html", form=form, book_list=book_list, books=books, selected_books=selected_books)




@app.route("/add_list", methods=["GET", "POST"])
@login_required
def add_list():
    form = CreateListForm()
    selected_books = []

    if request.method == "POST":
        book_ids = request.form.getlist("selected_books")  
        selected_books = Book.query.filter(Book.id.in_(book_ids)).all()  

        if form.validate_on_submit():
            new_list = BookList(
                name=form.name.data,
                user_id=current_user.id,
                is_public=form.is_public.data
            )
            db.session.add(new_list)
            db.session.commit()


            new_list.books.extend(selected_books)
            db.session.commit()

            flash("✅ Book list created successfully!", "success")
            return redirect(url_for("profile"))  


    books = Book.query.all()

    return render_template("add_list.html", form=form, books=books, selected_books=selected_books)




@app.route("/search_books", methods=["GET"])
@login_required
def search_books():
    query = request.args.get("q", "").strip()
    books = Book.query.filter(
        (Book.title.ilike(f"%{query}%")) |
        (Book.author.ilike(f"%{query}%"))
    ).limit(10).all()

    books_json = [{"id": book.id, "title": book.title, "author": book.author} for book in books]
    return jsonify(books_json)
