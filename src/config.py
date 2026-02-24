import os
from dotenv import load_dotenv
from src.exceptions import MissingConfigurationError

load_dotenv()

AVALAI_API_KEY = os.getenv("AVALAI_API_KEY")
if not AVALAI_API_KEY:
    raise MissingConfigurationError("AVALAI_API_KEY is not set in the .env file.")

API_BASE_URL = "https://api.avalai.ir/v1"