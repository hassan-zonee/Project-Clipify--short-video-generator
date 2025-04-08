import os
import uuid
from datetime import datetime

def delete_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    else:
        print(f"File not found: {file_path}")


def generate_unique_filename(path, extension=".mp4"):
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{unique_id}{extension}"
    file_path = os.path.join(path, filename)

    return file_path
