from flask import Flask, render_template, redirect, url_for, request  # type: ignore
from flask_bootstrap import Bootstrap5  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # type: ignore
from sqlalchemy import Integer, String, Text  # type: ignore
from flask_wtf import FlaskForm  # type: ignore
from wtforms import StringField, SubmitField  # type: ignore
from wtforms.validators import DataRequired, URL  # type: ignore
from flask_ckeditor import CKEditor, CKEditorField  # type: ignore
from datetime import datetime  # type: ignore
import smtplib
import os


# Set your constant variables for email and password right here:
SMTP_EMAIL = ""
APP_PASSWORD = ""

SECRET_KEY = os.urandom(24)
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
Bootstrap5(app)
ckeditor = CKEditor(app)


class MakePost(FlaskForm):
    title = StringField("Post title", validators=[DataRequired()])
    subtitle = StringField("Post subtitle", validators=[DataRequired()])
    author = StringField("Post author", validators=[DataRequired()])
    img_url = StringField("Post image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Post content", validators=[DataRequired()])
    submit = SubmitField("Submit")


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Blog/instance/posts.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    data = db.session.execute(db.select(BlogPost).order_by(BlogPost.id)).scalars()
    if data is None:
        return 404
    posts = [i for i in data]
    return render_template("index.html", all_posts=posts)


# TODO: Add a route so that you can click on individual posts.
@app.route("/post/<int:post_id>")
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.session.execute(
        db.select(BlogPost).where(BlogPost.id == post_id)
    ).scalar()
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route("/add-post", methods=["GET", "POST"])
def add_new_post():
    form = MakePost()
    post_id = request.args.get("post_id")
    post = db.session.execute(
        db.select(BlogPost).where(BlogPost.id == post_id)
    ).scalar()
    if request.method == "POST" and form.validate_on_submit():
        post_data = request.form
        new_post = BlogPost(
            title=post_data["title"],
            subtitle=post_data["subtitle"],
            date=datetime.today().strftime("%B %d, %Y"),
            body=post_data["body"],
            author=post_data["author"],
            img_url=post_data["img_url"],
        )
        db.session.add(new_post)
        db.session.commit()
        post_id = db.session.execute(
            db.select(BlogPost.id).where(BlogPost.title == post_data["title"])
        ).scalar()
        return redirect("/post/<int:post_id>", post_id=post_id)
    return render_template("make-post.html", form=form, post=post)


@app.route("/edit-post/<int:post_id>", methods=["GET", "PUT"])
def edit_post(post_id):
    form = MakePost()
    post_to_update = db.session.execute(
        db.select(BlogPost).where(BlogPost.id == post_id)
    ).scalar()
    if post_to_update == None:
        return 404
    else:
        form.title.data = post_to_update.title
        form.subtitle.data = post_to_update.subtitle
        form.body.data = post_to_update.body
        form.author.data = post_to_update.author
        form.img_url.data = post_to_update.img_url
        if request.method == "PUT" and form.validate_on_submit():
            post_data = request.form
            post_to_update.title = post_data["title"]
            post_to_update.subtitle = post_data["subtitle"]
            post_to_update.date = datetime.today().strftime("%Y-%m-%d")
            post_to_update.body = post_data["body"]
            post_to_update.author = post_data["author"]
            post_to_update.img_url = post_data["img_url"]
            db.session.commit()
            return redirect("/post/<int:post_id>", post_id=post_id)
    return render_template("make-post.html", form=form, post=post_to_update)


@app.route("/delete-post/<int:post_id>", methods=["GET", "DELETE"])
def delete_post(post_id):
    post_to_delete = db.session.execute(
        db.select(BlogPost).where(BlogPost.id == post_id)
    ).scalar()
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(SMTP_EMAIL, APP_PASSWORD)
        connection.sendmail(SMTP_EMAIL, SMTP_EMAIL, email_message)


if __name__ == "__main__":
    app.run(debug=True)
