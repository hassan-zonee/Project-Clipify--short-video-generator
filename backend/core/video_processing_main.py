import yt_dlp
from moviepy import VideoFileClip, AudioFileClip
import time
from . import video_clipping, utils, constants, video_reframing
import librosa
import soundfile as sf


def process_video(url):
    #downloaded_video = download_video(url)
    #extracted_audio = video_clipping.extract_audio(downloaded_video, utils.generate_unique_filename(constants.temp_path, '.wav'))
    #clips = video_clipping.generate_video_clips(downloaded_video, extracted_audio)
    #transcription = video_clipping.transcribe_audio(extracted_audio)
    
    input_video_path = constants.temp_path + "/test2.mp4"
    output_video_path = utils.generate_unique_filename(constants.generated_clips_path, '.mp4')
    video_reframing.get_processed_video(input_video_path, output_video_path)
    



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


def merge_audio_with_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    final_video = video.with_audio(audio)
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

    video.close()
    audio.close()
    
    return output_path

def extract_audio(video_path, output_audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(output_audio_path, fps=16000, codec='pcm_s16le')
    
    audio, sr = librosa.load(output_audio_path, sr=16000, mono=True)
    sf.write(output_audio_path, audio, sr)
    
    video.close()
    
    return output_audio_path