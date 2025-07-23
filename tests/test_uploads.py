import os
import tempfile
import pytest
from utils.uploads import validate_upload_file, UPLOADS_DIR


def create_temp_file(extension: str, size_bytes: int) -> str:
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    fd, path = tempfile.mkstemp(suffix=extension, dir=UPLOADS_DIR)
    with os.fdopen(fd, "wb") as tmp:
        tmp.write(b"0" * size_bytes)
    return path


def test_accept_csv_up_to_10mb():
    path = create_temp_file(".csv", 10 * 1024 * 1024)
    assert validate_upload_file(path) is True
    os.remove(path)


def test_accept_xlsx_up_to_10mb():
    path = create_temp_file(".xlsx", 10 * 1024 * 1024)
    assert validate_upload_file(path) is True
    os.remove(path)


def test_reject_invalid_extension():
    path = create_temp_file(".exe", 1024)
    with pytest.raises(ValueError):
        validate_upload_file(path)
    os.remove(path)


def test_reject_file_larger_than_10mb():
    path = create_temp_file(".csv", 11 * 1024 * 1024)
    with pytest.raises(ValueError):
        validate_upload_file(path)
    os.remove(path)


def test_reject_file_outside_uploads():
    fd, path = tempfile.mkstemp(suffix=".csv")
    with os.fdopen(fd, "wb") as tmp:
        tmp.write(b"0" * 1024)
    with pytest.raises(ValueError):
        validate_upload_file(path)
    os.remove(path) 