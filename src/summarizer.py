from openai_service import OpenAIClient


def summarize_pdf(file_path: str):
    ai = OpenAIClient()
    file = ai.upload_file(file_path)
    summary_response = ai.create_response(model="gpt-4.1", file_id=file.id, prompt="Summarize this pdf file.")

    return summary_response