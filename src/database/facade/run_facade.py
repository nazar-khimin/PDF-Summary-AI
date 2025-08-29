from database.models import DimFiles, DimModels, DimPrompts, FactRuns
from database.dto import RunDTO, map_run_row_to_dto
from database.database import with_db_session
from sqlalchemy import text
from datetime import datetime
from typing import Optional

@with_db_session
def save_run(pdf_path: str, model_name: str, system_prompt: str, user_prompt: str, output: str, db=None):
    """
    Builds and persists a FactRuns record with linked dimension entities.
    """
    run = FactRuns(
        file=DimFiles(filename=pdf_path),
        model=DimModels(name=model_name),
        prompt=DimPrompts(system_prompt=system_prompt, user_prompt=user_prompt),
        output_length=len(output),
        created_at=datetime.now()
    )
    db.add(run)

@with_db_session
def get_run_by_id(run_id: int, db=None) -> Optional[RunDTO]:
    """
    Retrieves a single FactRuns record by ID and maps it to a RunDTO.
    """
    query = text("""
        SELECT
            fr.id              AS run_id,
            f.filename         AS filepath,
            m.name             AS model_name,
            p.system_prompt,
            p.user_prompt,
            e.created_at       AS evaluation_time,
            fr.output_length,
            fr.processing_time,
            fr.created_at      AS run_time
        FROM fact_runs fr
        LEFT JOIN dim_files f       ON fr.file_id = f.id
        LEFT JOIN dim_models m      ON fr.model_id = m.id
        LEFT JOIN dim_prompts p     ON fr.prompt_id = p.id
        LEFT JOIN dim_evaluations e ON e.run_id = fr.id
        WHERE fr.id = :run_id
    """)
    result = db.execute(query, {"run_id": run_id}).fetchone()
    return map_run_row_to_dto(result) if result else None
