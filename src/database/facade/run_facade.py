from database.database import with_db_session
from database.models import DimModels, DimFiles, DimPrompts
from database.models.fact_runs import FactRuns
from datetime import datetime

@with_db_session
def save_run(pdf_path: str, model_name: str, system_prompt: str, user_prompt: str, output, db=None):

    # Create related objects
    file_record = DimFiles(filename=pdf_path)
    model_record = DimModels(name=model_name)
    prompt_record = DimPrompts(system_prompt=system_prompt, user_prompt=user_prompt)

    # Create FactRuns with relationships
    run_record = FactRuns(
        file=file_record,
        model=model_record,
        prompt=prompt_record,
        output_length=len(output),
        created_at=datetime.now()
    )

    # Add everything in one go
    db.add(run_record)