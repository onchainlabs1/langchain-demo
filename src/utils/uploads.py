import os
from typing import Any

MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {".csv", ".xlsx"}
UPLOADS_DIR = os.path.abspath("uploads")


def validate_upload_file(file_path: str, base_dir: str = UPLOADS_DIR) -> bool:
    """
    Validates if the uploaded file meets security requirements:
    - Allowed extension (.csv, .xlsx)
    - Size up to 10 MB
    - Path must be inside the uploads directory
    """
    _, extension = os.path.splitext(file_path)
    if extension.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("File extension not allowed. Only CSV or XLSX.")
    if os.path.getsize(file_path) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValueError("File exceeds the maximum size of 10 MB.")
    abs_path = os.path.abspath(file_path)
    if not abs_path.startswith(base_dir):
        raise ValueError("File is outside the allowed uploads directory.")
    return True 