import os, shutil
from typing import BinaryIO
UPLOAD_DIR = "uploads"; os.makedirs(UPLOAD_DIR, exist_ok=True)
def save_upload(fileobj: BinaryIO, filename: str) -> str:
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f: shutil.copyfileobj(fileobj, f)
    return path
