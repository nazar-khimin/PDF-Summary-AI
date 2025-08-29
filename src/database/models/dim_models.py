from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class DimModels(Base):
    __tablename__ = 'dim_models'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    provider = Column(String(50), nullable=True)
    type = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    
    # Relationships
    runs = relationship("FactRuns", back_populates="model")
    evaluations = relationship("DimEvaluations", back_populates="model")
