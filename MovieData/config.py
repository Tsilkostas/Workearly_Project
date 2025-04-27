import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

def get_credentials() -> tuple[str, str]:
    """Safely retrieves API credentials from environment variables."""
    api_key = os.getenv("TMDB_API_KEY")
    token = os.getenv("API_READ_ACCESS_TOKEN")
    
    if not api_key or not token:
        raise RuntimeError(
            "Missing TMDb credentials. "
            "Ensure .env contains TMDB_API_KEY and TMDB_READ_ACCESS_TOKEN"
        )
    return api_key, token

API_KEY, API_READ_ACCESS_TOKEN = get_credentials()