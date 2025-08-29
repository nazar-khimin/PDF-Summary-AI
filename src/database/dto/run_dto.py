from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class RunDTO:
    run_id: int
    filepath: str
    model_name: str
    system_prompt: str
    user_prompt: str
    evaluation_time: Optional[datetime]
    output_length: int
    processing_time: Optional[float]
    run_time: datetime

def map_run_row_to_dto(row) -> RunDTO:
    return RunDTO(
        run_id=row.run_id,
        filepath=row.filepath,
        model_name=row.model_name,
        system_prompt=row.system_prompt,
        user_prompt=row.user_prompt,
        evaluation_time=row.evaluation_time,
        output_length=row.output_length,
        processing_time=row.processing_time,
        run_time=row.run_time
    )