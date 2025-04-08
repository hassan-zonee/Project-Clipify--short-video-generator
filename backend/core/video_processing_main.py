import yt_dlp
from moviepy import VideoFileClip
import time
from . import video_clipping
from . import utils
from . import constants


def process_video(url):
    downloaded_video = download_video(url)
    extracted_audio = video_clipping.extract_audio(downloaded_video, utils.generate_unique_filename(constants.temp_path, '.wav'))
    clips = video_clipping.generate_video_clips(downloaded_video, extracted_audio)
    #transcription = video_clipping.transcribe_audio(extracted_audio)
    
    return "results"



def download_video(url: str):
    print('downloading...')
    output_path = utils.generate_unique_filename(constants.video_download_path, extension=".mp4")
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