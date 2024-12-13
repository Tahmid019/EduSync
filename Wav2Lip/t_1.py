
import cv2
import face_recognition


def detect_face_intervals(video_path):
    video_capture = cv2.VideoCapture(video_path)
    face_intervals = []
    no_face_intervals = []

    if not video_capture.isOpened():
        print("Error: Could not open video.")
        return [], []

    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / frame_rate
    face_detected = False
    start_time = 0

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break

        current_time = video_capture.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # Current time in seconds
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)

        if face_locations and not face_detected:
            if start_time != 0:  # If it's not the very beginning of the video
                no_face_intervals.append((start_time, current_time - start_time))
            face_detected = True
            start_time = current_time
        elif not face_locations and face_detected:
            face_detected = False
            face_intervals.append((start_time, current_time - start_time))
            start_time = current_time
        elif not face_locations and not face_detected:
            continue

    if face_detected:
        face_intervals.append((start_time, duration - start_time))
    else:
        no_face_intervals.append((start_time, duration - start_time))

    video_capture.release()
    return face_intervals, no_face_intervals



print(detect_face_intervals('/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/video.mp4'))
