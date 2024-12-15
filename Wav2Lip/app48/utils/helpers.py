import os
import ffmpeg


def convert_mp4_to_wav(mp4_file_path, PROCESSED_FOLDER):
    try:
        base_name = os.path.splitext(os.path.basename(mp4_file_path))[0]
        wav_file_path = os.path.join(PROCESSED_FOLDER, f"{base_name}.wav")
        ffmpeg.input(mp4_file_path).output(wav_file_path, format='wav').run(overwrite_output=True)
        return wav_file_path
    except ffmpeg.Error as e:
        print(f"ffmpeg error: {e.stderr.decode()}")
    return None

def merge_audio_with_silent_video(silent_video, input_audio, output_video):
    input_video = ffmpeg.input(silent_video)
    input_audio = ffmpeg.input(input_audio)
    output_stream = ffmpeg.output(input_video, input_audio, output_video, vcodec='copy', acodec='aac', strict='experimental')
    ffmpeg.run(output_stream, overwrite_output=True)

def save_file(file, folder, filename):
    path = os.path.join(folder, filename)
    file.save(path)
    return path

def find_file(directory, filename):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            print(f"[[==>{os.path.join(root, filename)}<=== ]]")
            return True
    return False

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
  