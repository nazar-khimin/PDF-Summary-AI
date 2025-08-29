from database.facade.run_facade import save_run
from eval.summary_jsonl_generator import generate_summary_jsonl
from openroute import OpenRouterClient
from openai_service import OpenAIClient


def summarize_pdf(pdf_file_path: str):
    model = "gpt-5"
    gpt_4o_mini = "gpt-4o-mini"

    ai = OpenAIClient()
    pdf_file = ai.upload_file(pdf_file_path, "user_data")
    summary_response = ai.create_response(model=model, file_id=pdf_file.id)
    eval_file_path = generate_summary_jsonl(summary_response, model)

    eval_file = ai.upload_file(eval_file_path, "user_data")
    ai.run_evaluation(eval_file.id, gpt_4o_mini)

    return summary_response

def openroute_summarize_pdf(pdf_file_path: str):

    client = OpenRouterClient()

    model = "google/gemma-3-27b-it"
    system_prompt = "You are an expert assistant that extracts insights from complex PDFs, including tables and images."
    user_prompt = "Summarize all key findings, preserving tables and images context where relevant."
    response = client.summarize_pdf(
        model=model,
        pdf_path=pdf_file_path,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )
    output = response.choices[0].message.content
    save_run(pdf_file_path, model, system_prompt, user_prompt, output)
    return output