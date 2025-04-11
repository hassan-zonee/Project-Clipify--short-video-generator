import yt_dlp
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import time
from . import video_clipping, utils, constants, video_reframing
import librosa
import soundfile as sf
import wave
import json
from vosk import Model, KaldiRecognizer
import string as str


def process_video(url):
    #downloaded_video = download_video(url)
    #extracted_audio = video_clipping.extract_audio(downloaded_video, utils.generate_unique_filename(constants.temp_path, '.wav'))
    #clips = video_clipping.generate_video_clips(downloaded_video, extracted_audio)
    #transcription = video_clipping.transcribe_audio(extracted_audio)
    
    
    input_video_path = constants.temp_path + "/test2.mp4"
    output_video_path = utils.generate_unique_filename(constants.generated_clips_path, '.mp4')
    
    # reframe video
    reframed_video = video_reframing.reframe_video(input_video_path, output_video_path)
    
    # extract audio
    audio_path = utils.generate_unique_filename(constants.temp_path, '.wav')
    extract_audio(input_video_path, audio_path)
    
    # generate subtitles
    subtitles = utils.create_subtitle_chunks(transcribe_audio(audio_path))
    
    # add subtitles
    
    add_subtitles_to_video(reframed_video, subtitles, output_video_path)
    
    utils.delete_file(audio_path)
    utils.delete_file(reframed_video)
    
    
    

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



def transcribe_audio(audio_path, model_path="././vosk-model-small-en-us-0.15"):
    wf = wave.open(audio_path, "rb")
    
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        raise ValueError("Audio must be WAV format: mono, 16-bit, 16kHz")

    # Load model
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, wf.getframerate())
    recognizer.SetWords(True)

    results = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            results.append(result)

    final_result = json.loads(recognizer.FinalResult())
    results.append(final_result)
    
    wf.close()
    
    return results


def add_subtitles_to_video(video_path, subtitles, output_path):
    video = VideoFileClip(video_path)
    clips = [video]

    for sub in subtitles:
        text = sub['text'].upper()
        txt_clip = (
            TextClip(text=text, font_size=15, color='yellow', font='././FunnelSans-Bold.ttf', margin=(None, 20))
            .with_position(("center", 0.7), relative=True)
            .with_start(sub['start'])
            .with_duration(sub['end'] - sub['start'])
        )
        clips.append(txt_clip)

    final = CompositeVideoClip(clips)
    final.write_videofile(output_path, codec='libx264', audio_codec='aac')