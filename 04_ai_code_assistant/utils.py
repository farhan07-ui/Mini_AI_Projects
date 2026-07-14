from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

def ai_code_assistant(task, code, language="Python"):
    prompt = f"""
You are an expert software engineer.

Task:
{task}

Programming Language:
{language}

Code:
{code}

Provide a clear and accurate response.
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