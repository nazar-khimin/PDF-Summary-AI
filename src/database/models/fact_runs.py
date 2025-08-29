from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from . import DimFiles, DimModels, DimPrompts, DimEvaluations
from .base import Base


class FactRuns(Base):
    __tablename__ = 'fact_runs'

    id = Column(Integer, primary_key=True, autoincrement=True)

    file_id = Column(Integer, ForeignKey('dim_files.id'), nullable=True)
    model_id = Column(Integer, ForeignKey('dim_models.id'), nullable=True)
    prompt_id = Column(Integer, ForeignKey('dim_prompts.id'), nullable=True)

    output_length = Column(Integer, nullable=True)
    processing_time = Column(Float, nullable=True)  # in seconds
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    file: "DimFiles" = relationship("DimFiles", back_populates="runs")
    model: "DimModels" = relationship("DimModels", back_populates="runs")
    prompt: "DimPrompts" = relationship("DimPrompts", back_populates="runs")
    evaluations: list["DimEvaluations"] = relationship("DimEvaluations", back_populates="run")

    def __init__(self, file=None, model=None, prompt=None, output_length=None, processing_time=None, created_at=None):
        super().__init__()
        self.file = file
        self.model = model
        self.prompt = prompt
        self.output_length = output_length
        self.processing_time = processing_time
        self.created_at = created_at or datetime.now()
