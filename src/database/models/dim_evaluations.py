from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class DimEvaluations(Base):
    __tablename__ = 'dim_evaluations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(Integer, ForeignKey('fact_runs.id'), nullable=False)
    model_id = Column(Integer, ForeignKey('dim_models.id'), nullable=False)
    score = Column(Float, nullable=False)
    reasoning = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    run = relationship("FactRuns", back_populates="evaluations")
    model = relationship("DimModels", back_populates="evaluations")
