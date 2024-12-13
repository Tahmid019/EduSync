import face_recognition
from moviepy.editor import VideoFileClip
import ffmpeg
from pydub import AudioSegment



def detect_face_intervals(video_path):
    clip = VideoFileClip(video_path)
    face_intervals = []
    # no_face_intervals = []

    duration = clip.duration
    face_detected = True
    start_time = 0
    

    def process_frame(frame, t):
        # i = 1
        nonlocal face_detected, start_time
        current_time = t

        # Convert frame to RGB
        rgb_frame = frame[:, :, ::-1]
        
        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        print(f"face_locations: {face_locations} || len_face_locations: {len(face_locations)}")
        # l = len(face_locations)
        face_intervals.append((start_time, current_time - start_time, len(face_locations)))
        start_time = current_time
        if len(face_locations) == 0:
            face_detected = False
        else:
            face_detected = True 
        

        # if len(face_locations) == 0:
        #     # if start_time != 0:  # If it's not the very beginning of the video
        #         # print(f"{len(face_locations) and (face_detected)}")
        #     face_intervals.append((start_time, current_time - start_time, len(face_locations)))
        #     # face_detected = True
            
        # else:
        #     # face_detected = False
        #     # print(l)
        #     # print(f"{len(face_locations) and (face_detected)}")
        #     face_intervals.append((start_time, current_time - start_time, len))
        #     start_time = current_time

    
    # print(f"frame: {frame} || t: {t}")
    i = 1
    # Process the video frame by frame
    for t, frame in clip.iter_frames(fps=1, with_times=True, dtype='uint8'):
        process_frame(frame, t)
        # print(f"process: {process_frame(frame, t)}")
        # print(f"frame: {frame} || t: {t}")
        print(i)
        i += 1

    # Finalize intervals
    if face_detected:
        face_intervals.append((start_time, duration - start_time, 1))
    else:
        face_intervals.append((start_time, duration - start_time, 0))

    return face_intervals



def merge_intervals(intervals, gap=1):
    if not intervals:
        return []

    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0])

    merged_intervals = []

    # Initialize variables
    current_start, current_duration, current_val = intervals[0]
    current_end = current_start + current_duration

    for start, duration, val in intervals[1:]:
        if val == current_val and start <= current_end + gap:
            current_end = max(current_end, start + duration)
        else:
            merged_intervals.append((current_start, current_end - current_start, current_val))
            current_start = start
            current_end = start + duration
            current_val = val

    # Append the last interval
    merged_intervals.append((current_start, current_end - current_start, current_val))

    return merged_intervals


vid = '/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/video.mp4'

face_intervals = detect_face_intervals(vid)
print(f"Face Intervals: {face_intervals}")
# print(f"No Face Intervals: {no_face_intervals}")

print(f"len Face Intervals: {len(face_intervals)}")
# print(f"len No Face Intervals: {len(no_face_intervals)}")

# print(f"face: {face_intervals[0]}")
# print(f"len face: {len(face_intervals[0])}")
test = merge_intervals(face_intervals)
print(f"Face Merge Intervals: {test}")
print(f"Face Merge Intervals: {test[0]}")
print(f"Face Merge Intervals: {test[0][1]}")


