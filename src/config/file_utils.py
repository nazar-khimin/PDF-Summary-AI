import os


def check_file_exists(file_path: str) -> None:
    """
    Validates that the given file path exists and is a file.
    Raises FileNotFoundError if the file is missing.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
