from flask import Flask, render_template, request
from utils import ai_code_assistant

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        task = request.form["task"]
        language = request.form["language"]
        code = request.form["code"]

        result = ai_code_assistant(task, code, language)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)