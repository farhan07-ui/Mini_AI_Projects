from flask import Flask, render_template, request
import os
from utils import generate_caption

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    image = request.files["image"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    image.save(filepath)

    caption = generate_caption(filepath)

    return render_template(
        "index.html",
        caption=caption,
        image=image.filename
    )


if __name__ == "__main__":
    app.run(debug=True)