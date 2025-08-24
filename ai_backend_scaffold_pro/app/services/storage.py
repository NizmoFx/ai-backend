import os, shutil
from .config import settings

def save_upload(file_obj, filename: str) -> str:
    path = os.path.join(settings.storage_dir, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file_obj, f)
    return path
