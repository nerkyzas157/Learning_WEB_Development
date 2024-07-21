from flask import Flask, render_template, redirect, url_for, request  # type: ignore
from flask_bootstrap import Bootstrap5  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # type: ignore
from sqlalchemy import Integer, String, Float, func  # type: ignore
from flask_wtf import FlaskForm  # type: ignore
from wtforms import StringField, IntegerField, SubmitField  # type: ignore
from wtforms.validators import DataRequired, URL  # type: ignore
import requests  # type: ignore
import os
from dotenv import dotenv_values  # type: ignore
import json


config = dotenv_values(".env")
tmdb_key = config["TMDB_API_KEY"]
tmdb_token = config["TMDB_ACCESS_TOKEN"]

# TMDB headers, parameters and URL
headers = {"accept": "application/json", "Authorization": f"Bearer {tmdb_token}"}
parameters = {
    "query": "placeholder",
    "include_adult": "true",
    "language": "en-US",
    "page": "1",
}
SEARCH_URL = "https://api.themoviedb.org/3/search/movie"


SECRET_KEY = os.urandom(24)
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
Bootstrap5(app)


class NewForm(FlaskForm):
    title = StringField("Movie title", validators=[DataRequired()])
    submit = SubmitField("Search")


class EditForm(FlaskForm):
    ranking = IntegerField("Your Ranking Out of 10", validators=[DataRequired()])
    review = StringField("Your review", validators=[DataRequired()])
    submit = SubmitField("Done")


# Creating database
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Top_Movies/instance/movies.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Defining table
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, autoincrement=True)
    review: Mapped[str] = mapped_column(String(250), autoincrement=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


# Creating table schema in the database
with app.app_context():
    db.create_all()

    def add_movie_if_not_exists(movie):
        existing_movie = db.session.query(Movie).filter_by(title=movie.title).first()
        if existing_movie is None:
            db.session.add(movie)
            db.session.commit()

    # Adding data into the db
    new_movie = Movie(
        title="Interstellar",
        year=2014,
        description="When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.",
        rating=8.7,
        ranking=1,
        review="This is my favourite movie. I love the sci-fi idea and how the story wrangles.",
        img_url="https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p10543523_p_v8_as.jpg",
    )
    add_movie_if_not_exists(new_movie)

    second_movie = Movie(
        title="The Dark Knight",
        year=2008,
        description="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        rating=9.0,
        ranking=2,
        review="Character development and what actors had to go through to film this movie, is just astonishing. Not to mention the soundtrack.",
        img_url="https://m.media-amazon.com/images/S/pv-target-images/e9a43e647b2ca70e75a3c0af046c4dfdcd712380889779cbdc2c57d94ab63902.jpg",
    )
    add_movie_if_not_exists(second_movie)

    third_movie = Movie(
        title="Django Unchained",
        year=2012,
        description="With the help of a German bounty-hunter, a freed slave sets out to rescue his wife from a brutal plantation owner in Mississippi.",
        rating=8.5,
        ranking=3,
        review="In my opinion, the best Q. Tarantino movie. Loved the characters, dialogue and cinematics.",
        img_url="https://m.media-amazon.com/images/M/MV5BMjIyNTQ5NjQ1OV5BMl5BanBnXkFtZTcwODg1MDU4OA@@._V1_FMjpg_UX1000_.jpg",
    )
    add_movie_if_not_exists(third_movie)


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.ranking.asc()))
    all_movies = result.scalars().all()
    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = NewForm()
    if request.method == "POST" and form.validate_on_submit():
        parameters["query"] = request.form["title"]
        response = requests.get(SEARCH_URL, params=parameters, headers=headers)
        data = response.json()["results"]
        return redirect(url_for("select", data=json.dumps(data)))
    return render_template("add.html", form=form)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditForm()
    if request.method == "POST" and form.validate_on_submit():
        movie_id = request.args.get("id")
        movie_to_update = db.get_or_404(Movie, movie_id)
        movie_to_update.ranking = request.form["ranking"]
        movie_to_update.review = request.form["review"]
        db.session.commit()
        return redirect(url_for("home"))
    movie_id = request.args.get("id")
    selected_movie = db.get_or_404(Movie, movie_id)
    return render_template("edit.html", movie=selected_movie, form=form)


@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/select")
def select():
    data = request.args.get("data")
    data = json.loads(data)
    return render_template("select.html", data=data)


@app.route("/load")
def load():
    new_movie = Movie(
        title=request.args.get("title"),
        year=request.args.get("year").split("-")[0],
        description=request.args.get("description"),
        rating=round(float(request.args.get("rating")), 1),
        ranking=db.session.execute(func.max(Movie.ranking)).scalar() + 1,
        review="",
        img_url="https://image.tmdb.org/t/p/original" + request.args.get("img_url"),
    )
    db.session.add(new_movie)
    db.session.commit()
    movie_id = db.session.execute(
        db.select(Movie.id).where(Movie.title == request.args.get("title"))
    ).scalar()
    return redirect(url_for("edit", id=movie_id))


if __name__ == "__main__":
    app.run(debug=True)
