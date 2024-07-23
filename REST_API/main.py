from flask import Flask, jsonify, render_template, request  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # type: ignore
from sqlalchemy import Integer, String, Boolean, func  # type: ignore
import random as r
from dataclasses import dataclass

"""

View API documentation here: https://documenter.getpostman.com/view/37174670/2sA3kVn2LU
or render documentation template.

"""

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///REST_API/instance/cafes.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
@dataclass
class Cafe(db.Model):
    id: int
    name: str
    map_url: str
    img_url: str
    location: str
    seats: str
    has_toilet: bool
    has_wifi: bool
    has_sockets: bool
    can_take_calls: bool
    coffee_price: str

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()
    print(db.session.execute(func.max(Cafe.id)).scalar())


@app.route("/documentation")
def documentation():
    return render_template("documentation.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def random():
    cafe_details = []
    try:
        rand_index = r.randint(1, int(db.session.execute(func.max(Cafe.id)).scalar()))
    except TypeError:
        return {"response": "ID Not Found"}, 404
    else:
        if request.method == "GET":
            data = db.session.execute(
                db.select(Cafe).where(Cafe.id == rand_index)
            ).scalar()
            for i in data:
                cafe_details.append(i)
            response = {"cafe_details": cafe_details}
            return jsonify(response)
        else:
            return {"response": "Wrong HTTP Method"}, 404


@app.route("/all", methods=["GET"])
def all():
    cafe_details = []
    if request.method == "GET":
        data = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars()
        if data is None:
            return jsonify({"response": "Cafe not found"}), 404
        for i in data:
            cafe_details.append(i)
        response = {"cafe_details": cafe_details}
        return jsonify(response)
    else:
        return {"response": "Wrong HTTP Method"}, 404


@app.route("/search", methods=["GET"])
def search():
    cafe_details = []
    location = request.args.get("loc", type=str)
    if request.method == "GET":
        data = db.session.execute(
            db.select(Cafe).where(Cafe.location == location)
        ).scalars()
        if data is None:
            return jsonify({"response": "No cafe found"}), 404
        for i in data:
            cafe_details.append(i)
        response = {"cafe_details": cafe_details}
        return jsonify(response)
    else:
        return {"response": "Wrong HTTP Method"}, 404


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add():
    if request.method == "POST":
        new_cafe = Cafe(
            name=request.form("name", type=str),
            map_url=request.form("map_url", type=str),
            img_url=request.form("img_url", type=str),
            location=request.form("location", type=str),
            seats=request.form("seats", type=str),
            has_toilet=request.form("has_toilet", type=bool),
            has_wifi=request.form("has_wifi", type=bool),
            has_sockets=request.form("has_sockets", type=bool),
            can_take_calls=request.form("can_take_calls", type=bool),
            coffee_price=request.form("coffee_price", type=str),
        )
        db.session.add(new_cafe)
        db.session.commit()
        response = {"response": "success"}
        return jsonify(response)
    else:
        return {"response": "Wrong HTTP Method"}, 404


# HTTP PUT/PATCH - Update Record
@app.route("/update-cafe/<cafe_id>", methods=["PUT"])
def update_cafe(cafe_id):
    api_key = request.args.get("api_key", type=str)
    if api_key != "TopSecretAPIKey":
        return {"response": "You do not have sufficient permissions."}, 403
    cafe_id = request.args.get("cafe_id", type=str)
    cafe_to_update = db.session.execute(
        db.select(Cafe).where(Cafe.id == cafe_id)
    ).scalar()
    if cafe_to_update == None:
        return {"response": "ID Not Found"}, 404
    else:
        if request.method == "PUT":
            cafe_to_update.name = request.args.get("name", type=str)
            cafe_to_update.map_url = request.args.get("map_url", type=str)
            cafe_to_update.img_url = request.args.get("img_url", type=str)
            cafe_to_update.location = request.args.get("location", type=str)
            cafe_to_update.seats = request.args.get("seats", type=str)
            cafe_to_update.has_toilet = request.args.get("has_toilet", type=bool)
            cafe_to_update.has_wifi = request.args.get("has_wifi", type=bool)
            cafe_to_update.has_sockets = request.args.get("has_sockets", type=bool)
            cafe_to_update.can_take_calls = request.args.get(
                "can_take_calls", type=bool
            )
            cafe_to_update.coffee_price = request.args.get("coffee_price", type=str)
            db.session.commit()
            response = {"response": "success"}
            return jsonify(response)
        else:
            return {"response": "Wrong HTTP Method"}, 404


@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    cafe_id = request.args.get("cafe_id", type=str)
    price_to_update = db.session.execute(
        db.select(Cafe).where(Cafe.id == cafe_id)
    ).scalar()
    if price_to_update == None:
        return {"response": "ID Not Found"}, 404
    else:
        if request.method == "PATCH":
            price_to_update.price = request.args.get("new_price", type=str)
            response = {"response": "success"}
            return jsonify(response)
        else:
            return {"response": "Wrong HTTP Method"}, 404


# HTTP DELETE - Delete Record
@app.route("/delete-cafe/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api_key", type=str)
    if api_key != "TopSecretAPIKey":
        return {"response": "You do not have sufficient permissions."}, 403
    cafe_id = request.args.get("cafe_id", type=str)
    cafe_to_delete = db.session.execute(
        db.select(Cafe).where(Cafe.id == cafe_id)
    ).scalar()
    if cafe_to_delete == None:
        return {"response": "ID Not Found"}, 404
    else:
        if request.method == "DELETE":
            db.session.delete(cafe_to_delete)
            db.session.commit()
            response = {"response": "success"}
            return jsonify(response)
        else:
            return {"response": "Wrong HTTP Method"}, 404


if __name__ == "__main__":
    app.run()
