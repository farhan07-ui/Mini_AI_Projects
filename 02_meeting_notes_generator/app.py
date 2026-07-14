from flask import Flask, render_template, request
from utils import extract_text, generate_meeting_notes
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "transcript" not in request.files:
        return "No file uploaded."

    file = request.files["transcript"]

    if file.filename == "":
        return "No file selected."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)

    transcript = extract_text(filepath)

    notes = generate_meeting_notes(transcript)

    return render_template("index.html", result=notes)


if __name__ == "__main__":
    app.run(debug=True)