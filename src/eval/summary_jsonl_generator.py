import json
from dataclasses import dataclass, asdict
from typing import List
from datetime import datetime
from pathlib import Path
import tempfile


@dataclass
class SummaryRecord:
    generated_summary: str
    model_name: str


class JsonlGenerator:
    def __init__(self, prefix: str = "summary"):
        """
        Create a temp file with a readable, deterministic name.
        Example: /tmp/summary_2025-08-25_22-57-44.jsonl
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{prefix}_{timestamp}.jsonl"
        temp_dir = Path(tempfile.gettempdir())
        self.filepath = temp_dir / filename
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def write_records(self, summary_records: List[SummaryRecord]) -> str:
        """Write records to the JSONL file."""
        with self.filepath.open("w", encoding="utf-8") as f:
            for record in summary_records:
                wrapped = {"item": asdict(record)}
                f.write(json.dumps(wrapped, ensure_ascii=False) + "\n")
        return self.filepath.as_posix()


def generate_summary_jsonl(summary: str, model_name: str) -> str:
    """
    Create a SummaryRecord and write it to a cleanly named temp JSONL file.
    """
    record = SummaryRecord(summary, model_name)
    generator = JsonlGenerator(prefix="summary")
    return generator.write_records([record])
