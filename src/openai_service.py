from openai import OpenAI
from openai.types import FileObject
import logging
from config.env_variables import OPENAI_API_KEY
from config.file_utils import check_file_exists

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

    def upload_file(self, file_path: str) -> FileObject:
        """
        Uploads a file to OpenAI and returns the file object.
        """
        check_file_exists(file_path)
        file = self.client.files.create(
            file=open(file_path, "rb"),
            purpose="user_data",
            expires_after={
                "anchor": "created_at",
                "seconds": 3600
            }
        )

        return file


    def create_response(self, model: str, file_id: str, prompt: str):
        """
        Creates a response using a file and a text prompt.
        """
        response =  self.client.responses.create(
            model=model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_file", "file_id": file_id},
                        {"type": "input_text", "text": prompt},
                    ],
                }
            ]
        )

        return response.output_text
