import face_recognition
import numpy as np
from moviepy.editor import VideoFileClip

def remove_audio(input_video):
    input_stream = ffmpeg.input(input_video)
    base_name = os.path.splitext(os.path.basename(input_video))[0]
    output_video = os.path.join(PROCESSED_FOLDER, f"{base_name}_no_audio.mp4")
    output_stream = ffmpeg.output(input_stream, output_video, c='copy', an=None)
    ffmpeg.run(output_stream, overwrite_output=True)
    return output_video

#Process a single frame of video to detect face presence and update the intervals.
def process_frame(frame, t, buffer, face_detected, start_time, buffer_size):

    current_time = t

    # Convert frame to RGB
    rgb_frame = frame[:, :, ::-1]
    
    # Detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    
    buffer.append(len(face_locations) > 0)
    if len(buffer) > buffer_size:
        buffer.pop(0)

    # Check if face is consistently detected in the buffer
    detected = np.mean(buffer) > 0.25

    # Update intervals based on face detection status
    if detected:
        if face_detected is False or face_detected is None:
            # Append interval for no-face region
            if face_detected is False:
                intervals.append((start_time, current_time - start_time, 0))
            # Update start time
            start_time = current_time
            face_detected = True
    else:
        if face_detected is True or face_detected is None:
            # Append interval for face region
            if face_detected is True:
                intervals.append((start_time, current_time - start_time, 1))
            # Update start time
            start_time = current_time
            face_detected = False

    return face_detected, start_time

def detect_face_intervals(video_path):
    clip = VideoFileClip(video_path)
    face_intervals = []
    
    duration = clip.duration
    face_detected = None
    start_time = 0

    # Smooth the frame processing by using a buffer
    buffer_size = 7
    buffer = []

    # Process the video frame by frame
    for t, frame in clip.iter_frames(fps=1, with_times=True, dtype='uint8'):
        face_detected, start_time = process_frame(frame, t, buffer, face_detected, start_time, buffer_size)

    # Finalize intervals
    if face_detected is not None:
        face_intervals.append((start_time, duration - start_time, 1 if face_detected else 0))

    return face_intervals

def split_video(video_path, face_intervals, output_prefix):
    split_files = []
    try:
        for i, (start, duration, value) in enumerate(face_intervals):
            output_path = f"{output_prefix}_fiv-{value}_{i}.mp4"
            ffmpeg.input(video_path, ss=start, t=duration).output(output_path).run(overwrite_output=True)
            print(output_path)
            
            split_files.append(output_path)
        return split_files
    except Exception as e:
        print(f"Error splitting video: {e}")
        return []

def process_videos(final, PROCESSED_FOLDER, utc_str):
    input_files = []
    print("=======vid clipping...")

    for video in final:
        print(f"clip === {video}")
        try:
            probe = ffmpeg.probe(video)
            # Check if the clip has a duration and is not empty or corrupted
            if probe['streams'][0]['duration'] != 'N/A':
                input_files.append(video)
                print(f"Clip loaded: {video}, vid.filename: {os.path.basename(video)}, duration: {probe['streams'][0]['duration']}")
            else:
                print(f"Clip {video} is empty or corrupted.")
        except ffmpeg.Error as e:
            print(f"Error processing video {video}: {e}")
            # return jsonify({'error': f"Error processing video {video}: {e}"}), 500

    if not input_files:
        print("No valid clips to concatenate.")
        # return jsonify({'error': 'No valid clips to concatenate'}), 500

    try:
        print(f"=======Concat : {input_files}")
        concat_file_path = os.path.join(PROCESSED_FOLDER, f"merged_final_video_{utc_str}.mp4")

        # Create a text file with all input files for concatenation
        with open('input_files.txt', 'w') as f:
            for file in input_files:
                f.write(f"file '{file}'\n")

        # Run FFmpeg to concatenate the videos
        ffmpeg.input('input_files.txt', format='concat', safe=0).output(concat_file_path, c='copy').run()

        print(f"Final clip saved to: {concat_file_path}")
        return concat_file_path
        # return jsonify({'message': 'Video concatenation successful', 'path': concat_file_path}), 200
    except ffmpeg.Error as e:
        print(f"Error during concatenation: {e}")
        


