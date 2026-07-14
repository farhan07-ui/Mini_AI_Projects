import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_ai(prompt):
    """
    Sends a prompt to Groq AI and returns the response.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert email writing assistant. "
                        "Always generate clear, professional, well-formatted emails."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


def generate_email(prompt):
    ai_prompt = f"""
Write a professional email based on the following request.

Request:
{prompt}

Requirements:
- Generate a suitable subject line.
- Write a complete email.
- Use a professional tone.
- Format the email properly.
"""
    return ask_ai(ai_prompt)


def rewrite_email(email):
    ai_prompt = f"""
Rewrite the following email.

Requirements:
- Correct grammar and spelling.
- Improve clarity.
- Keep the original meaning.
- Make it sound professional.

Email:
{email}
"""
    return ask_ai(ai_prompt)


def change_tone(email, tone):
    ai_prompt = f"""
Rewrite the following email in a {tone} tone.

Keep the meaning unchanged.

Email:
{email}
"""
    return ask_ai(ai_prompt)