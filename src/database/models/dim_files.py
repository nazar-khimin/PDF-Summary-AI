from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class DimFiles(Base):
    __tablename__ = 'dim_files'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(500), nullable=False)
    size_bytes = Column(BigInteger, nullable=False)
    page_count = Column(Integer, nullable=False)
    token_count = Column(Integer, nullable=True)
    image_count = Column(Integer, nullable=True)
    table_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to fact table
    runs = relationship("FactRuns", back_populates="file")
