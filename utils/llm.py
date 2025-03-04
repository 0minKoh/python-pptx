from os import environ as env
from dotenv import load_dotenv
from google import genai

def call_llm_api(prompt: str) -> str:
    load_dotenv()
    GEMINI_API_KEY = env.get("GEMINI_API_KEY")
    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=[prompt])
    return response.text