import librosa
import soundfile as sf
from moviepy import VideoFileClip
from vosk import Model, KaldiRecognizer
import wave
import json
from . import utils
from . import constants


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
    
    temp_json_path = utils.generate_unique_filename(constants.temp_path, '.json')
    with open(temp_json_path, "w") as json_file:
        json.dump(results, json_file, indent=4)

    return temp_json_path


def extract_audio(video_path, output_audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(output_audio_path, fps=16000, codec='pcm_s16le')
    
    audio, sr = librosa.load(output_audio_path, sr=16000, mono=True)
    sf.write(output_audio_path, audio, sr)
    
    return output_audio_path
