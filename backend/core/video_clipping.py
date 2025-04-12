import random
import numpy as np
import librosa
import soundfile as sf
from moviepy import VideoFileClip
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import MidTermFeatures
from . import utils, constants


def generate_video_clips(video_path, audio_path):
    video = VideoFileClip(video_path)
    
    try:    
        clip_paths = []
        segments = extract_key_segments(audio_path)
        print(f"🎯 Total segments found: {len(segments)}")
        random.shuffle(segments)
        segments = segments[: min(30, len(segments))]
        
        for i, (start, end) in enumerate(segments):
            print(f"Segment {i+1}: Start={start}s, End={end}s, Duration={end - start}s")
        
        
        for i, (start, end) in enumerate(segments):
            filename = utils.generate_unique_filename(constants.temp_path, '.mp4')
            subclip = video.subclipped(start, min(end, video.duration))
            subclip.write_videofile(filename, codec="libx264", audio_codec="aac")
            clip_paths.append(filename)
    except Exception as e:
        print(e)
        
    finally:
        video.close()

    return clip_paths


def extract_key_segments(audio_path, threshold=.3, duration=30):
    [fs, x] = audioBasicIO.read_audio_file(audio_path)
    mt, st, mt_names = MidTermFeatures.mid_feature_extraction(x, fs, 
                                                              1 * fs,
                                                              1 * fs,
                                                              0.05 * fs,
                                                              0.05 * fs)
    
    energy_index = 1  # Energy is typically at index 1
    energy = mt[energy_index]
    
    # Normalize energy
    energy = (energy - np.min(energy)) / (np.max(energy) - np.min(energy))
    
    # Identify high-energy segments
    high_energy_times = []
    for i, val in enumerate(energy):
        clip_duration = random.randint(duration-10, duration)
        if val >= threshold:
            start = i
            end = i + int(clip_duration / 1)  # step is 1 sec
            high_energy_times.append((start, min(end, len(energy))))
    
    # Remove overlapping segments
    merged = []
    for start, end in high_energy_times:
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
    
    # Convert to seconds and filter out segments shorter than 10 seconds
    segments = [(s, e) for s, e in merged if (e - s) >= 15]
    
    # Convert the frame-based start/end to actual time in seconds
    time_segments = [(s * 1.0, e * 1.0) for s, e in segments]  # assuming 1 frame = 1 second
    
    return time_segments





