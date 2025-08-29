from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class DimPrompts(Base):
    __tablename__ = 'dim_prompts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    system_prompt = Column(Text, nullable=True)
    user_prompt = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to fact table
    runs = relationship("FactRuns", back_populates="prompt")
