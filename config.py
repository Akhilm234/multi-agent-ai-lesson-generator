
import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

# Use the same model that worked in your connection test
GEMINI_MODEL = "gemini-3.8-flash"

# Initialize Gemini
client = genai.Client(api_key=API_KEY)
