import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.8-flash"


def run_agent(user_request):

    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=user_request
            )

            return response.text

        except Exception as e:

            error_text = str(e)

            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < 2:
                    print(
                        f"Gemini is busy. "
                        f"Retrying ({attempt + 1}/2)..."
                    )
                    time.sleep(8)
                    continue

            return (
                "TASKORA couldn't reach Gemini right now.\n\n"
                f"Error: {error_text}"
            )