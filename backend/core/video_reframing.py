import cv2
import dlib
import numpy as np
from collections import deque, Counter
from . import constants, video_processing_main, utils


predictor_path = "././shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)


def get_processed_video(input_video_path, output_video_path):
    reframed_video_path = utils.generate_unique_filename(constants.temp_path, '.mp4')
    reframed_video = reframe_video(input_video_path, reframed_video_path)
    
    extracted_audio_path = utils.generate_unique_filename(constants.temp_path, '.wav')
    extracted_audio = video_processing_main.extract_audio(input_video_path, extracted_audio_path)
    
    video_processing_main.merge_audio_with_video(reframed_video_path, extracted_audio_path, output_video_path)
    
    utils.delete_file(reframed_video)
    utils.delete_file(extracted_audio)
    
    return output_video_path


def reframe_video(input_video_path, output_video_path):
    
    print("Reframing started!")

    cap = cv2.VideoCapture(input_video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    output_width = frame_height * 9 // 16
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (output_width, frame_height))

    last_speaker_face = None

    speaker_history = deque(maxlen=10)
    center_history = deque(maxlen=15) 
    frame_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        speaking_face = None
        current_max_lip_distance = 0

        for face in faces:
            landmarks = predictor(gray, face)
            top_lip = landmarks.parts()[48]
            bottom_lip = landmarks.parts()[54]

            lip_distance = euclidean_distance((top_lip.x, top_lip.y), (bottom_lip.x, bottom_lip.y))

            if lip_distance > current_max_lip_distance:
                current_max_lip_distance = lip_distance
                speaking_face = face

        if speaking_face:
            speaker_history.append(speaking_face)

        frame_counter += 1

        if frame_counter % 10 == 0 and speaker_history:
            face_counts = Counter([(f.left(), f.top(), f.right(), f.bottom()) for f in speaker_history])
            most_common_face, count = face_counts.most_common(1)[0]

            if count >= 5:  # consistency percent
                for f in speaker_history:
                    if (f.left(), f.top(), f.right(), f.bottom()) == most_common_face:
                        # 🟡 Check if speaker has changed
                        new_speaker_face = f
                        if last_speaker_face is None or (
                            last_speaker_face.left() != new_speaker_face.left() or
                            last_speaker_face.top() != new_speaker_face.top() or
                            last_speaker_face.right() != new_speaker_face.right() or
                            last_speaker_face.bottom() != new_speaker_face.bottom()
                        ):
                            # 🟢 Speaker changed → clear smoothing history
                            center_history.clear()
                            x, y, w, h = (new_speaker_face.left(), new_speaker_face.top(),
                                        new_speaker_face.width(), new_speaker_face.height())
                            face_center = (x + w // 2, y + h // 2)
                            center_history.append(face_center)

                        last_speaker_face = new_speaker_face
                        break

        if last_speaker_face:
            (x, y, w, h) = (last_speaker_face.left(), last_speaker_face.top(),
                            last_speaker_face.width(), last_speaker_face.height())
            
            face_center = (x + w // 2, y + h // 2)
            center_history.append(face_center)
        else:
            out.write(frame)
            continue

        avg_x = int(np.mean([c[0] for c in center_history]))
        avg_y = int(np.mean([c[1] for c in center_history]))
        smoothed_center = (avg_x, avg_y)

        crop_x1 = max(0, smoothed_center[0] - output_width // 2)
        crop_x2 = min(frame_width, smoothed_center[0] + output_width // 2)

        if crop_x2 - crop_x1 < output_width:
            if crop_x1 == 0:
                crop_x2 = output_width
            else:
                crop_x1 = frame_width - output_width

        crop_y1 = 0
        crop_y2 = frame_height

        cropped_frame = frame[crop_y1:crop_y2, crop_x1:crop_x2]
        cropped_frame_resized = cv2.resize(cropped_frame, (output_width, frame_height))

        out.write(cropped_frame_resized)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Reframing completed!")
    
    return output_video_path


def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)