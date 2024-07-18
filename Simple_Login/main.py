from flask import Flask, render_template, redirect  # type: ignore
from flask_wtf import FlaskForm  # type: ignore
from wtforms import StringField, PasswordField, SubmitField  # type: ignore
from wtforms.validators import DataRequired, Email, Length  # type: ignore
from flask_wtf.csrf import CSRFProtect  # type: ignore
from flask_bootstrap import Bootstrap4  # type: ignore


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=64)]
    )

    submit = SubmitField("Log In")


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
csrf = CSRFProtect(app)
bootstrap = Bootstrap4(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@email.com" and form.password.data == "12345678":
            return redirect("/success")
        else:
            return redirect("/denied")
    return render_template("login.html", form=form)


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/denied")
def denied():
    return render_template("denied.html")


if __name__ == "__main__":
    app.run(debug=True)
