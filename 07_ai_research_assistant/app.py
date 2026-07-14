from flask import Flask, render_template, request
from ollama_util import ask_local_model

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    question = ""
    
    if request.method == "POST":
        if "question" in request.form:
            question = request.form["question"]
            answer = ask_local_model(question)
            
    return render_template(
        "index.html",
        question=question,
        answer=answer
    )

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/pdf", methods=["POST"])
def pdf():
    answer = ""
    
    if "pdf" in request.files:
        file = request.files["pdf"]
        
        if file.filename != "":
            try:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""

                prompt = f"Summarize this research paper concisely:\n\n{text}"
                # Get the summary from local Ollama
                answer = ask_local_model(prompt)
            except Exception as e:
                answer = f"Error processing PDF: {str(e)}"

    return render_template(
        "index.html",
        answer=answer
    )

if __name__ == "__main__":
    app.run(debug=True)