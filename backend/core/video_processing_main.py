import yt_dlp
from moviepy import VideoFileClip
import time
from . import video_clipping
from . import utils
from . import constants


def process_video(url):
    #downloaded_video = download_video(url)
    #extracted_audio = video_clipping.extract_audio(video_path, generate_unique_filename(temp_path, '.wav'))
    
    downloaded_video = constants.video_download_path + "/20250408_183601_c20b36ba-5e9d-416f-8049-c597984996dd.mp4"
    extracted_audio = constants.temp_path + '/20250408_190306_6329673e-3c28-49df-8273-e4492e548376.wav'
    
    transcription = video_clipping.transcribe_audio(extracted_audio)
    return transcription



def download_video(url: str):
    print('downloading...')
    output_path = generate_unique_filename(constants.video_download_path, extension=".mp4")
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