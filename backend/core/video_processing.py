import uuid
import os
from datetime import datetime
import yt_dlp

def process_video(url):
    download_video(url)

def download_video(url: str):
    """
    Download the video from the provided URL and store it temporarily with a unique filename.
    :param url: The URL of the video to download.
    :return: None
    """

    print('downloading...')
    output_path = generate_unique_filename(extension=".mp4")
    ydl_opts = {
        'format': 'bestvideo[height<=480]+bestaudio/best',
        'outtmpl': output_path,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path




def delete_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    else:
        print(f"File not found: {file_path}")


def generate_unique_filename(extension=".mp4"):
    """
    Generate a unique filename for the video download using UUID and timestamp.
    :param extension: File extension (e.g., '.mp4')
    :return: Unique file name as a string
    """
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{unique_id}{extension}"
    file_path = os.path.join("media/videos", filename)

    return file_path
