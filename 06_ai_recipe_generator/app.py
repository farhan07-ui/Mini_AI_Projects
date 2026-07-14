from flask import Flask, render_template, request
from utils import generate_recipe

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    recipe = ""

    if request.method == "POST":
        ingredients = request.form["ingredients"]

        recipe = generate_recipe(ingredients)

    return render_template(
        "index.html",
        recipe=recipe
    )


if __name__ == "__main__":
    app.run(debug=True)