import os

from dotenv import load_dotenv

load_dotenv()

class Env:
    @staticmethod
    def fetch(key: str, default: str = None) -> str:
        value = os.getenv(key, default)
        if value is None:
            raise EnvironmentError(f"Missing required environment variable: '{key}'")
        return value

# Access environment variables via Env class
OPENROUTER_API_KEY = Env.fetch("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = Env.fetch("OPENROUTER_BASE_URL")
OPENAI_API_KEY = Env.fetch("OPENAI_API_KEY")