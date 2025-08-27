from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.env_variables import DATABASE_FILE_PATH
from .models import Base

# SQLite database URL
DATABASE_URL = f"sqlite:///{DATABASE_FILE_PATH}"

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables if they don't exist"""
    Base.metadata.create_all(bind=engine)

def get_db_session():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def init_database():
    """Initialize database with tables"""
    create_tables()
