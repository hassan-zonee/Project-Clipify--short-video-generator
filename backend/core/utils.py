import os
import uuid
from datetime import datetime
import random
import wave
from vosk import Model, KaldiRecognizer
import json


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


def create_subtitle_chunks(vosk_results, words=3, max_duration=4.0):
    subtitles = []
    chunk = []
    start_time = None

    for res in vosk_results:
        if 'result' not in res:
            continue
        for word in res['result']:
            if not chunk:
                start_time = word['start']
            chunk.append(word)
            duration = word['end'] - start_time
            max_words = random.randint(words//2, words)
            if len(chunk) >= max_words or duration >= max_duration:
                text = " ".join([w['word'] for w in chunk])
                subtitles.append({
                    "start": chunk[0]['start'],
                    "end": chunk[-1]['end'],
                    "text": text
                })
                chunk = []
    # Handle last chunk
    if chunk:
        text = " ".join([w['word'] for w in chunk])
        subtitles.append({
            "start": chunk[0]['start'],
            "end": chunk[-1]['end'],
            "text": text
        })
    return subtitles



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