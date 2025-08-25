from eval.summary_jsonl_generator import generate_summary_jsonl
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



# if __name__ == "__main__":
#     gpt_5 = "gpt-5"
#     gpt_4o_mini = "gpt-4o-mini"
#
#     ai = OpenAIClient()
#     pdf_file = ai.upload_file('/Users/nkhimin/PycharmProjects/PDF-Summary-AI/test_data/text_what_is_earth_science.pdf', "user_data")
#     summary_response = ai.create_response(model=gpt_5, file_id=pdf_file.id)
#     eval_file_path = generate_summary_jsonl(summary_response, gpt_5)
#
#     eval_file = ai.upload_file(eval_file_path, "evals")
#     ai.run_evaluation(eval_file.id, gpt_4o_mini)