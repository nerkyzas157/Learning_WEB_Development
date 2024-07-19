from flask import Flask, render_template, redirect  # type: ignore
from flask_bootstrap import Bootstrap5  # type: ignore
from flask_wtf import FlaskForm  # type: ignore
from wtforms import StringField, SelectField, SubmitField  # type: ignore
from wtforms.validators import DataRequired, URL  # type: ignore
import csv
import os


SECRET_KEY = os.urandom(24)
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
Bootstrap5(app)

COFFEE_RATING = ["✘", "☕️", "☕️☕️", "☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️☕️☕️"]
WIFI_RATING = ["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"]
POWER_COUNT = ["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"]


class CafeForm(FlaskForm):
    cafe = StringField("Cafe name", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired(), URL()])
    open = StringField("Open", validators=[DataRequired()])
    close = StringField("Close", validators=[DataRequired()])
    coffee = SelectField("Coffee", choices=COFFEE_RATING)
    wifi = SelectField("Wifi", choices=WIFI_RATING)
    power = SelectField("Power", choices=POWER_COUNT)
    submit = SubmitField("Submit")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open(
            "cafe-data.csv",
            mode="a",
            newline="",
            encoding="utf-8",
        ) as csv_file:
            writer_object = csv.writer(csv_file)
            new_data = [
                form.cafe.data,
                form.location.data,
                form.open.data,
                form.close.data,
                form.coffee.data,
                form.wifi.data,
                form.power.data,
            ]
            writer_object.writerow(new_data)
            csv_file.close()
    return render_template("add.html", form=form)


@app.route("/cafes")
def cafes():
    with open(
        "cafe-data.csv",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template("cafes.html", cafes=list_of_rows)


if __name__ == "__main__":
    app.run(debug=True)
