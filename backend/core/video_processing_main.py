import yt_dlp
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import random
from . import utils, constants, video_reframing, video_clipping_nlp_based
import librosa
import soundfile as sf
import string as str


def process_video(url):
    downloaded_video = download_video(url)
    extracted_audio = extract_audio(downloaded_video, utils.generate_unique_filename(constants.temp_path, '.wav'))
    clips = video_clipping_nlp_based.generate_video_clips(downloaded_video, extracted_audio, constants.temp_path)
    
    utils.delete_file(extracted_audio)
    utils.delete_file(downloaded_video)
    
    processed_clips = []
    
    for clip in clips:
        input_video_path = clip
        output_video_path = utils.generate_unique_filename(constants.generated_clips_path, '.mp4')
        
        # reframe video
        reframed_video = video_reframing.reframe_video(input_video_path, utils.generate_unique_filename(constants.temp_path, '.mp4'))
        if(is_valid_video(reframed_video) == False):
            utils.delete_file(input_video_path)
            utils.delete_file(reframed_video)
            continue
        
        # extract audio
        audio_path = utils.generate_unique_filename(constants.temp_path, '.wav')
        extract_audio(input_video_path, audio_path)
        
        # generate subtitles
        subtitles = utils.create_subtitle_chunks(utils.transcribe_audio(audio_path))
        
        #merge audio to reframed video
        audio_video_merge_path = merge_audio_with_video(reframed_video, audio_path, utils.generate_unique_filename(constants.temp_path, '.mp4'))
        
        # add subtitles
        add_subtitles_to_video(audio_video_merge_path, subtitles, output_video_path)
        processed_clips.append(output_video_path)
        
        utils.delete_file(audio_path)
        utils.delete_file(audio_video_merge_path)
        utils.delete_file(reframed_video)
        utils.delete_file(clip)
        
    return processed_clips
    

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




def add_subtitles_to_video(video_path, subtitles, output_path):
    video = VideoFileClip(video_path)
    clips = [video]

    for sub in subtitles:
        text = sub['text'].upper()
        
        color = 'white'
        random_number = random.randint(0, 20)
        if(random_number >= 17):
            color = 'yellow'
        elif(random_number >= 14):
            color = 'lightgreen'
        
        txt_clip = (
            TextClip(text=text, font_size=15, color=color, font='././PoetsenOne-Regular.ttf', margin=(None, 20))
            .with_position(("center", 0.7), relative=True)
            .with_start(sub['start'])
            .with_duration(sub['end'] - sub['start'])
        )
        clips.append(txt_clip)

    final = CompositeVideoClip(clips)
    final.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    video.close()
    
    
def is_valid_video(path):
    try:
        clip = VideoFileClip(path)
        duration = clip.duration
        clip.close()
        return duration is not None and duration > 0
    except Exception as e:
        print(f"[ERROR] Invalid video file: {e}")
        return False