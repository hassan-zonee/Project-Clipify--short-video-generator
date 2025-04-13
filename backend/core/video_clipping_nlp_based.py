import random
from moviepy import VideoFileClip
from . import utils


def generate_video_clips(video_path, audio_path, clips_directory):
    video = VideoFileClip(video_path)
    
    try:    
        clip_paths = []
        segments = utils.transcribe_audio(audio_path)
        sentences = parse_sentences(segments)
        print(f"🎯 Total sentences found: {len(sentences)}")
        random.shuffle(sentences)
        sentences = sentences[: min(30, len(sentences))]
        
        for i in range(len(sentences)):
            sen = sentences[i]
            print(f"Segment {i+1}: Start={sen['start']}s, End={sen['end']}s, Duration={sen['end'] - sen['start']}s")
        
        
        for sen in sentences:
            start = sen['start']
            end = sen['end']
            filename = utils.generate_unique_filename(clips_directory, '.mp4')
            subclip = video.subclipped(start, min(end, video.duration))
            subclip.write_videofile(filename, codec="libx264", audio_codec="aac")
            clip_paths.append(filename)
    except Exception as e:
        print(e)
        
    finally:
        video.close()

    return clip_paths
    

def parse_sentences(results, min_segment_duration = 12):
    segments = []

    for res in results:
        words = res.get("result", [])
        if not words:
            continue

        start_time = words[0]["start"]
        end_time = words[-1]["end"]
        
        if(abs(end_time-start_time) < min_segment_duration):
            continue
        
        text = res.get("text", "").strip()

        if text:
            segments.append({
                "start": start_time,
                "end": end_time,
                "text": text
            })

    return segments
