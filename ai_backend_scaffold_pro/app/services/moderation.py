import os

ALLOWED_EXT = {".jpg",".jpeg",".png",".webp"}
MAX_BYTES = 10*1024*1024  # 10MB

def basic_checks(filepath: str):
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in ALLOWED_EXT:
        raise ValueError(f"Unsupported file type: {ext}")
    size = os.path.getsize(filepath)
    if size > MAX_BYTES:
        raise ValueError(f"File too large: {size} bytes")
    return True
