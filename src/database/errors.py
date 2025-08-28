"""Database-related exceptions and error handling."""


class DatabaseError(Exception):
    """Custom database exception for handling database operation failures."""
    
    def __init__(self, message: str, original_error=None):
        super().__init__(message)
        self.original_error = original_error