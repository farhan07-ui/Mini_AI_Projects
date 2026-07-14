from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_recipe(ingredients):

    prompt = f"""
You are a professional chef.

The user has these ingredients:

{ingredients}

Create a delicious recipe.

Give the output in this format:

Recipe Name:

Cooking Time:

Difficulty:

Ingredients Needed:

Step-by-step Instructions:

Chef Tips:

Keep it simple and practical.
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