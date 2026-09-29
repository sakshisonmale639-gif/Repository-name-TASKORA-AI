import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

MODEL = "gemini-2.5-flash"


def run_agent(user_request):
    response = client.models.generate_content(
        model=MODEL,
        contents=user_request
    )

    return response.text