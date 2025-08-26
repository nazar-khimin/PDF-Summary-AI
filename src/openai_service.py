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

    def upload_file(self, file_path: str, purpose) -> FileObject:
        """
        Uploads a file to OpenAI and returns the file object.
        """
        check_file_exists(file_path)
        file = self.client.files.create(
            file=open(file_path, "rb"),
            purpose=purpose,
            expires_after={
                "anchor": "created_at",
                "seconds": 3600
            }
        )

        return file

    def create_response(self, model: str, file_id: str):
        """
        Creates a response using a file and a text prompt.
        """
        response = self.client.responses.create(
            model=model,
            prompt={
                "id": "pmpt_68ab80d02b608194af3ce2f4e514bf9203ed347458a5e0f8",
                "version": "24",
                "variables": {
                    "reference_pdf": {
                        "type": "input_file",
                        "file_id": file_id,
                    },
                }
            }
        )

        return response.output_text

    def run_evaluation(self, file_id: str, model: str):
        eval_obj = self.client.evals.runs.create(
            eval_id="eval_68acc50485d88191b01de40d3ec69ff4",
            name="PDF Summary Evaluation",
            data_source={
                "type": "responses",
                "source": {"type": "file_id", "id": file_id},
                "model": model,
                "input_messages": {
                    "type": "template",
                    "template": [
                        {"role": "system", "content": "You are a helpful assistant. When given a prompt, return it exactly as-is. Do not rewrite, summarize, or improve it."},
                        {"role": "user", "content": "{{ item.generated_summary }}"},
                    ]
                }

            }
        )
        print(eval_obj)
