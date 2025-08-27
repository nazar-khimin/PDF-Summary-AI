from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class FactRuns(Base):
    __tablename__ = 'fact_runs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey('dim_files.id'), nullable=False)
    model_id = Column(Integer, ForeignKey('dim_models.id'), nullable=False)
    prompt_id = Column(Integer, ForeignKey('dim_prompts.id'), nullable=False)
    output_length = Column(Integer, nullable=False)
    processing_time = Column(Float, nullable=False)  # in seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    file = relationship("DimFiles", back_populates="runs")
    model = relationship("DimModels", back_populates="runs")
    prompt = relationship("DimPrompts", back_populates="runs")
    evaluations = relationship("DimEvaluations", back_populates="run")
