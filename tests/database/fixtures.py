import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base
from src.config.env_variables import TEST_DATABASE_FILE_PATH


@pytest.fixture
def db_session():
    """Create a temporary test database"""
    # Use test database file instead of in-memory
    test_db_path = TEST_DATABASE_FILE_PATH
    engine = create_engine(f"sqlite:///{test_db_path}")
    Base.metadata.drop_all(engine)  # Clean slate for each test run
    Base.metadata.create_all(engine)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = session_local()
    try:
        yield db
    finally:
        db.close()
    
    # Optionally clean up after tests (comment out if you want to keep the file)
    # if os.path.exists(test_db_path):
    #     os.remove(test_db_path)