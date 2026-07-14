from groq import Groq
from dotenv import load_dotenv
from pypdf import PdfReader
from docx import Document
import os

load_dotenv()

client = Groq()


def extract_text(filepath):
    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".txt":
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    elif extension == ".pdf":
        reader = PdfReader(filepath)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text

    elif extension == ".docx":
        doc = Document(filepath)

        text = ""

        for para in doc.paragraphs:
            text += para.text + "\n"

        return text

    return ""


def generate_meeting_notes(transcript):

    prompt = f"""
You are an expert AI meeting assistant.

Analyze the meeting transcript and generate:

1. Meeting Summary

2. Key Discussion Points

3. Decisions Made

4. Action Items
   - Responsible Person (if mentioned)
   - Deadline (if mentioned)

5. Next Steps

Transcript:

{transcript}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content