import face_recognition
from moviepy.editor import VideoFileClip

def detect_face_intervals(video_path):
    clip = VideoFileClip(video_path)
    face_intervals = []
    no_face_intervals = []

    duration = clip.duration
    face_detected = False
    start_time = 0

    def process_frame(frame, t):
        nonlocal face_detected, start_time
        current_time = t

        # Convert frame to RGB
        rgb_frame = frame[:, :, ::-1]
        
        # Detect faces in the frame
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
            return

    # Process the video frame by frame
    for t, frame in clip.iter_frames(fps=1, with_times=True, dtype='uint8'):
        process_frame(frame, t)

    # Finalize intervals
    if face_detected:
        face_intervals.append((start_time, duration - start_time))
    else:
        no_face_intervals.append((start_time, duration - start_time))

    return face_intervals, no_face_intervals

# Example usage
video_path = '/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/video.mp4'
face_intervals, no_face_intervals = detect_face_intervals(video_path)
print(f"Face Intervals: {face_intervals}")
print(f"No Face Intervals: {no_face_intervals}")
