from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class SearchForm(FlaskForm):
    query = StringField("Search", validators=[Length(max=255)])
    year = IntegerField("Year", validators=[NumberRange(min=1000, max=2100)], render_kw={"placeholder": "Year"})


    GENRES = [
        ("", "Any Genre"),  
        ("Science Fiction", "Science Fiction"),
        ("Fantasy", "Fantasy"),
        ("Mystery", "Mystery"),
        ("Romance", "Romance"),
        ("Horror", "Horror"),
        ("Biography", "Biography"),
        ("History", "History"),
        ("Philosophy", "Philosophy"),
        ("Poetry", "Poetry"),
    ]

    LANGUAGES = [
        ("", "Any Language"),  
        ("English", "English"),
        ("Bulgarian", "Bulgarian"),
        ("French", "French"),
        ("German", "German"),
        ("Spanish", "Spanish"),
        ("Italian", "Italian"),
    ]

    genre = SelectField("Genre", choices=GENRES)
    language = SelectField("Language", choices=LANGUAGES)


    sort_by = SelectField("Sort by", choices=[
        ("title", "Title"),
        ("author", "Author"),
        ("year", "Year"),
        ("rating", "Rating"),
        ("downloads", "Downloads")
    ])

    order = SelectField("Order", choices=[
        ("asc", "Ascending"),
        ("desc", "Descending")
    ])

    submit = SubmitField("Search")



class ReviewForm(FlaskForm):
    rating = IntegerField("Rating (1-5)", validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField("Comment", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Submit Review")

class CreateListForm(FlaskForm):
    name = StringField("List Name", validators=[DataRequired(), Length(max=255)])
    is_public = SelectField("Visibility", choices=[("1", "Public"), ("0", "Private")], coerce=int)
    submit = SubmitField("Create List")
