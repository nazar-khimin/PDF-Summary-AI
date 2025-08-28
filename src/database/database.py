from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from functools import wraps
import logging

from config.env_variables import DATABASE_FILE_PATH
from .models import Base
from .errors import DatabaseError

# Setup logger
logger = logging.getLogger(__name__)

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
    return SessionLocal()

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    db = get_db_session()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise DatabaseError(f"Database operation failed: {e}")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error: {e}")
        raise
    finally:
        db.close()


def with_db_session(func):
    """Decorator that provides a database session to the decorated function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with session_scope() as db:
            return func(*args, db=db, **kwargs)
    return wrapper

def init_database():
    """Initialize database with tables"""
    create_tables()
