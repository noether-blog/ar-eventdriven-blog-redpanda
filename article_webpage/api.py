from flask import Flask, request, make_response, render_template
from article_publisher import publish


app = Flask(__name__)


@app.route("/articles", methods=["POST"])
def articles():
    article = request.json
    publish(article)
    return "Article publié avec succès !"


@app.route("/", methods=["GET"])
def homepage():
    return render_template("article_publish.html")


if __name__ == "__main__":
    app.run(port=4200)
