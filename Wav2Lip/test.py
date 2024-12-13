import os
import ffmpeg
from pydub import AudioSegment, silence
import face_recognition
import cv2
import subprocess

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

def merge_intervals(intervals, gap=0.5):
    """
    Merges overlapping or closely adjacent intervals.
    
    Parameters:
    - intervals: List of tuples [(start, duration), ...]
    - gap: Maximum gap between intervals to consider them as adjacent
    
    Returns:
    - Merged list of intervals
    """
    if not intervals:
        return []

    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0])
    
    merged_intervals = []
    current_start, current_duration = intervals[0]
    current_end = current_start + current_duration

    for start, duration in intervals[1:]:
        if start <= current_end + gap:  # Overlapping or adjacent intervals
            current_end = max(current_end, start + duration)
        else:
            merged_intervals.append((current_start, current_end - current_start))
            current_start = start
            current_end = start + duration

    merged_intervals.append((current_start, current_end - current_start))

    return merged_intervals

def merge_audio_video(audio_path, video_path, output_path):
    try:
        # Probe video and audio to check streams
        video_probe = ffmpeg.probe(video_path)
        audio_probe = ffmpeg.probe(audio_path)

        print(f"Video streams: {video_probe['streams']}")
        print(f"Audio streams: {audio_probe['streams']}")

        input_video = ffmpeg.input(video_path)
        input_audio = ffmpeg.input(audio_path)

        # Explicitly map the video and audio streams
        ffmpeg.output(input_video, input_audio, output_path, vcodec='copy', acodec='aac', map=['0:v:0', '1:a:0']).run(overwrite_output=True)
    except ffmpeg.Error as e:
        print(f"ffmpeg error: {e.stderr.decode('utf-8')}")
    except Exception as e:
        print(f"Error merging audio and video: {e}")

def split_video(video_path, face_intervals, output_prefix):
    split_files = []
    try:
        for i, (start, duration) in enumerate(face_intervals):
            output_path = f"{output_prefix}_face_interval_{i}.mp4"
            ffmpeg.input(video_path, ss=start, t=duration).output(output_path).run(overwrite_output=True)
            split_files.append(output_path)
        return split_files
    except Exception as e:
        print(f"Error splitting video: {e}")
        return []

def split_audio(audio_path, face_intervals, output_prefix):
    audio = AudioSegment.from_wav(audio_path)
    split_files = []
    for i, (start, duration) in enumerate(face_intervals):
        output_path = f"{output_prefix}_face_interval_{i}.wav"
        end = start + duration
        chunk = audio[start*1000:end*1000]  # pydub works in milliseconds
        chunk.export(output_path, format="wav")
        split_files.append(output_path)
    return split_files

def merge_audio_video(audio_path, video_path, output_path):
    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(audio_path)
    ffmpeg.output(input_video, input_audio, output_path, vcodec='copy', acodec='aac').run(overwrite_output=True)

def concatenate_videos(video_files, output_path):
    ffmpeg.concat(*[ffmpeg.input(v) for v in video_files], v=1, a=1).output(output_path).run(overwrite_output=True)

video = '/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/video.mp4'
audio = '/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/video.wav'

print("Detecting face intervals...")
face_intervals, no_face_intervals = detect_face_intervals(video)
if not face_intervals:
    print("Error: No face intervals detected.")
    exit()

face_intervals = merge_intervals(face_intervals)
no_face_intervals = merge_intervals(no_face_intervals)

print("Splitting video based on face intervals...")
face_video_files = split_video(video, face_intervals, 'test11')
print("Splitting audio based on face intervals...")
face_audio_files = split_audio(audio, face_intervals, 'test12')

for video, audio in zip(face_video_files, face_audio_files):
    output_video_path = video.replace('face', 'face_lipsynced')
    print(f"Processing video: {video}, audio: {audio}")
    result = subprocess.run(
        ['python3', 'inference.py', '--checkpoint_path', 'checkpoints/wav2lip.pth',
         '--face', video, '--audio', audio, '--outfile', output_video_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300
    )
    print(f"Subprocess output: {result.stdout.decode('utf-8')}")
    print(f"Subprocess error: {result.stderr.decode('utf-8')}")

print("Merging non-face intervals...")
non_face_intervals = [(0, face_intervals[0][0])] + [(face_intervals[i][1], face_intervals[i+1][0]) for i in range(len(face_intervals) - 1)] + [(face_intervals[-1][1], int(cv2.VideoCapture(video).get(cv2.CAP_PROP_FRAME_COUNT)) / int(cv2.VideoCapture(video).get(cv2.CAP_PROP_FPS)))]
non_face_intervals = merge_intervals(non_face_intervals)

non_face_video_files = split_video(video, non_face_intervals, 'non_face')
non_face_audio_files = split_audio(audio, non_face_intervals, 'non_face_audio')

print("Merging audio and video for non-face intervals...")
merged_video_files = []
for non_face_video, non_face_audio in zip(non_face_video_files, non_face_audio_files):
    output_video_path = non_face_video.replace('non_face', 'merged')
    merge_audio_video(non_face_audio, non_face_video, output_video_path)
    merged_video_files.append(output_video_path)

final_video_files = sorted(face_video_files + merged_video_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
final_output_path = "final.mp4"
concatenate_videos(final_video_files, final_output_path)
