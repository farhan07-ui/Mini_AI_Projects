from flask import Flask, render_template, request
from utils import generate_email, rewrite_email, change_tone

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""

    if request.method == "POST":
        action = request.form.get("action")

        if action == "generate":
            prompt = request.form.get("prompt")
            result = generate_email(prompt)

        elif action == "rewrite":
            email = request.form.get("email")
            result = rewrite_email(email)

        elif action == "tone":
            email = request.form.get("email")
            tone = request.form.get("tone")
            result = change_tone(email, tone)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)