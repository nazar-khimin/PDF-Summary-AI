import base64
from pathlib import Path

from openai import OpenAI

from config.env_variables import OPENROUTER_BASE_URL, OPENROUTER_API_KEY

class OpenRouterClient:

    def __init__(self):
        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL
        )

    @staticmethod
    def encode_pdf_to_base64(pdf_path: str) -> str:
        """Encode PDF to base64 for OpenRouter file input."""
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode("utf-8")

    def summarize_pdf(
            self,
            model: str,
            pdf_path: str,
            system_prompt: str,
            user_prompt: str
    ):
        """
        Summarize a PDF including text, images, and tables.

        Args:
            model: OpenRouter model name
            pdf_path: path to the PDF
            system_prompt: instructions for the assistant
            user_prompt: user query / request
        """
        base64_pdf = self.encode_pdf_to_base64(pdf_path)
        data_url = f"data:application/pdf;base64,{base64_pdf}"

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {
                        "type": "file",
                        "file": {
                            "filename": Path(pdf_path).name,
                            "file_data": data_url,
                        },
                    },
                ],
            },
        ]

        plugins = [
            {
                "id": "file-parser",
                "pdf": {"engine": "mistral-ocr"}  # OCR engine handles images/tables
            }
        ]

        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            extra_body={"plugins": plugins},
        )