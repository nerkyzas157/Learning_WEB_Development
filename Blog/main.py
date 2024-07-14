from flask import Flask, render_template  # type: ignore
import requests  # type: ignore
import datetime

BLOG_URL = "https://api.npoint.io/c790b4d5cab58020d391"
YEAR = datetime.date.today().year
app = Flask(__name__)


@app.route("/")
def home():
    response = requests.get(BLOG_URL)
    content = response.json()
    return render_template("index.html", content=content, year=YEAR)


@app.route("/blog/<num>")
def get_blog(num):
    response = requests.get(BLOG_URL)
    blog_content = response.json()[int(num) - 1]
    return render_template("post.html", content=blog_content, year=YEAR)


if __name__ == "__main__":
    app.run()

# TODO: Add proper styling and more functionality
