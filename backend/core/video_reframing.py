import cv2
import face_alignment
import torch
import numpy as np

def reframe_video(input_path, output_path):
    # Load face-alignment with landmarks type 2D
    fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D, device='cpu')

    print("✅ Model Downloaded...")
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("❌ Failed to open video.")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        preds = fa.get_landmarks(frame)

        if preds is not None:
            for face_landmarks in preds:
                for (x, y) in face_landmarks:
                    cv2.circle(frame, (int(x), int(y)), 1, (0, 255, 0), -1)

        out.write(frame)
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"Processed {frame_count} frames...")

    cap.release()
    out.release()
    print("✅ Video saved with facial landmarks:", output_path)

