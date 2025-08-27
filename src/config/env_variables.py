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

# Database Configuration
DATABASE_FILE_PATH = Env.fetch("DATABASE_FILE_PATH", "inputs/db/pdf_summary_analytics.db")
TEST_DATABASE_FILE_PATH = Env.fetch("TEST_DATABASE_FILE_PATH", "inputs/db/test_pdf_summary_analytics.db")