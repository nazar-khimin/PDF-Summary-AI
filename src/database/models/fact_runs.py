from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class FactRuns(Base):
    __tablename__ = 'fact_runs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey('dim_files.id'), nullable=True)
    model_id = Column(Integer, ForeignKey('dim_models.id'), nullable=True)
    prompt_id = Column(Integer, ForeignKey('dim_prompts.id'), nullable=True)
    output_length = Column(Integer, nullable=True)
    processing_time = Column(Float, nullable=True)  # in seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    file = relationship("DimFiles", back_populates="runs")
    model = relationship("DimModels", back_populates="runs")
    prompt = relationship("DimPrompts", back_populates="runs")
    evaluations = relationship("DimEvaluations", back_populates="run")
