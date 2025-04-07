import uuid
import os
from datetime import datetime
import yt_dlp
from moviepy import VideoFileClip
import time

video_download_path = "media/videos"
generated_clips_path = "media/clips"

def process_video(url):
    #downloaded_video = download_video(url)
    downloaded_video = "media/videos/20250407_215320_33c2ff2e-1439-4fa2-a80c-658a11683c9d.mp4"
    print("Downloaded Video: ", downloaded_video)
    clips = split_video_into_clips(downloaded_video)

def download_video(url: str):
    print('downloading...')
    output_path = generate_unique_filename(video_download_path, extension=".mp4")
    ydl_opts = {
        'format': 'bestvideo[height<=480]+bestaudio/best',
        'outtmpl': output_path,
        'quiet': True,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path


def split_video_into_clips(video_path, clip_duration=30):
    video = VideoFileClip(video_path)
    total_duration = int(video.duration)
    print("duration: ", total_duration)

    clip_paths = []

    start_time = 0
    while start_time < total_duration:
        end_time = min(start_time + clip_duration, total_duration)
        clip = video.subclipped(start_time, end_time)
        output_path = generate_unique_filename(generated_clips_path, extension=".mp4")
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)
        clip_paths.append(output_path)
        start_time = end_time

    video.close()
    return clip_paths



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
