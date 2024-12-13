import face_recognition
from moviepy.editor import VideoFileClip
import ffmpeg
from pydub import AudioSegment



import time
from deep_translator import GoogleTranslator
from flask import Flask, logging, request, jsonify, send_from_directory
import os
import speech_recognition as sr
import ffmpeg
# from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment, silence
from flask_cors import CORS
import mysql.connector
import face_recognition
import cv2
import subprocess
from langdetect import detect, LangDetectException







import locale
locale.getpreferredencoding = lambda: "UTF-8"

# import locale
# locale.getpreferredencoding = lambda: "UTF-8"
#
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# app.config['"/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/face_face_test/upload"'] = "/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/face_face_test/upload"
# app.config['"/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/face_face_test/processed"'] = "/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/face_face_test/processed"
# app.config['"/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/face_face_test/transcriptions"'] = "/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/face_face_test/transcriptions"
# app.config['RESULTS'] = RESULTS

# MySQL configurations
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'nitsilchar'
# app.config['MYSQL_PASSWORD'] = 'TAR0HA=#UMF_'
# app.config['MYSQL_DB'] = 'lipsync'
# # app.config['MYSQL_HOST'] = 'localhost'
# # app.config['MYSQL_USER'] = 'root'
# # app.config['MYSQL_PASSWORD'] = ''
# # app.config['MYSQL_DB'] = 'lipsync'

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="nitsilchar",
        password="TAR0HA=#UMF_",
        database="lipsync"
        # host="localhost",
        # user="",
        # password="",
        # database="lipsync"
)






def transcribe_audio(file_path, sr_lang, retries=3):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_text = recognizer.record(source)
    src_lang = sr_lang + '-IN'
    attempt = 0
    while attempt < retries:
        try:
            text = recognizer.recognize_google(audio_text, language=src_lang)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            return ""
        except sr.RequestError as e:
            print(f"Attempt {attempt+1}: Could not request results from Google Speech Recognition service; {e}")
            attempt += 1
    return "Request failed after multiple attempts"

def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except LangDetectException as e:
        print(f"Language detection error: {e}")
        return ""

def convert_mp4_to_wav(mp4_file_path):
    try:
        base_name = os.path.splitext(os.path.basename(mp4_file_path))[0]
        wav_file_path = os.path.join("/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/face_face_test/processed", f"{base_name}.wav")
        ffmpeg.input(mp4_file_path).output(wav_file_path, format='wav').run(overwrite_output=True)
        return wav_file_path
    except ffmpeg.Error as e:
        print(f"ffmpeg error: {e.stderr.decode()}")
    return None

def translate_text_file(input_text, dest_language, src_lang):
    try:
        # detected_lang = src_lang 
        # if(detect_language != src_language):
        #         detected_lang = detect_language(input_text)

        translated = GoogleTranslator(source=src_lang, target=dest_language).translate(input_text)
        print(translated)
        return translated, src_lang
    except Exception as e:
        print(f"An error occurred: {e}")
    return "", ""

def text_to_speech_from_text(text, lang='bn', amplitude_change=0, pitch_change=0):
    tts = gTTS(text=text, lang=lang)
    temp_audio_path = os.path.join("/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/face_face_test/processed", "temp_output.mp3")
    tts.save(temp_audio_path)

    audio = AudioSegment.from_file(temp_audio_path)
    audio = audio + amplitude_change

    if pitch_change != 0:
        new_sample_rate = int(audio.frame_rate * (2.0 ** (pitch_change / 12.0)))
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
        audio = audio.set_frame_rate(44100)

    output_file_path = os.path.join("/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/face_face_test/processed", "translated_output.mp3")
    audio.export(output_file_path, format="mp3")
    return output_file_path

def remove_audio(input_video):
    input_stream = ffmpeg.input(input_video)
    base_name = os.path.splitext(os.path.basename(input_video))[0]
    output_video = os.path.join("/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/face_face_test/processed", f"{base_name}_no_audio.mp4")
    output_stream = ffmpeg.output(input_stream, output_video, c='copy', an=None)
    ffmpeg.run(output_stream, overwrite_output=True)
    return output_video

def merge_audio_with_silent_video(silent_video, input_audio, output_video):
    input_video = ffmpeg.input(silent_video)
    input_audio = ffmpeg.input(input_audio)
    output_stream = ffmpeg.output(input_video, input_audio, output_video, vcodec='copy', acodec='aac', strict='experimental')
    ffmpeg.run(output_stream, overwrite_output=True)

def detect_non_silent_regions(audio, silence_thresh=-60, min_silence_len=1000):
    silent_ranges = silence.detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    silent_ranges = [((start/1000), (stop/1000)) for start, stop in silent_ranges]  # Convert to seconds

    non_silent_ranges = []
    start = 0
    for start_time, end_time in silent_ranges:
        if start_time > start:
            non_silent_ranges.append((start, start_time))
        start = end_time
    if start < len(audio) / 1000:
        non_silent_ranges.append((start, len(audio) / 1000))
    return non_silent_ranges









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


def merge_intervals(intervals, gap=1):
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


def split_video(video_path, face_intervals, flag, output_prefix):
    split_files = []
    transcription_text = []
    try:
        for i, (start, duration) in enumerate(face_intervals):
            output_path = f"{output_prefix}_face_interval_{i}.mp4"
            print("===============")
            print("===============")
            print("===============")
            print(f"            {i}")
            print(f"{output_path}")
            print("===============")
            print("===============")
            print("===============")
            ffmpeg.input(video_path, ss=start, t=duration).output(output_path).run(overwrite_output=True)
            print(output_path)
            
            
            #===
            
            # if 'video' not in request.files:
            #     return jsonify({'error': 'No video file provided'}), 400

            # file = request.files['video']
            # if file.filename == '':
            #     return jsonify({'error': 'No selected file'}), 400
            # sr_lang = request.form.get('sr_lang')
            # print("==========srLang:", sr_lang)
            # dest_lang = request.form.get('dest_lang', 'bn')  # Default to Bengali if not provided
            # utc_str = request.form.get('utc_str')
            # print("=============", utc_str, "============")

            # file_path = os.path.join("/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/face_face_test/upload", file.filename)
            # file.save(file_path)
            sr_lang = 'hi'
            dest_lang = 'en'
            utc_str = "testing123"
            file_path = output_path  
            

            transcription_text = []

            try:
                # Convert video to WAV
                print("Calling convert_mp4_to_wav()")
                audio_file_path = convert_mp4_to_wav(file_path)
                if audio_file_path is None:
                    return 500

                print("Calling detect_non_silent_regions()")
                # Detect non-silent regions
                audio = AudioSegment.from_wav(audio_file_path)
                non_silent_regions = detect_non_silent_regions(audio)

                translated_audio_segments = []
                for start, end in non_silent_regions:
                    chunk = audio[start*1000:end*1000]  # pydub works in milliseconds
                    chunk.export("chunk.wav", format="wav")

                    # Transcribe the chunk
                    print(f"Calling transcribe_audio() for chunk {start}-{end}")
                    transcription = transcribe_audio("chunk.wav", sr_lang)
                    transcription_text.append(transcription)
                    if not transcription:
                        print(f"Skipping chunk {start}-{end}: Failed to transcribe audio")

                    # Translate the transcription
                    print(f"Calling translate_text_file() for chunk {start}-{end}")
                    translated_text, detected_lang = translate_text_file(transcription, dest_lang, sr_lang)
                    if not translated_text:
                        print(f"Skipping chunk {start}-{end}: Failed to translate transcription")

                    # Generate translated audio
                    print(f"Calling text_to_speech_from_text() for chunk {start}-{end}")
                    translated_audio_path = text_to_speech_from_text(translated_text, lang=dest_lang, pitch_change=0)
                    print("1")
                    translated_audio_segment = AudioSegment.from_file(translated_audio_path)
                    print("2")
                    translated_audio_segments.append((start, translated_audio_segment))
                    print("3")

                final_audio = AudioSegment.silent(duration=len(audio))

                # Overlay translated segments back into their original positions
                for start, segment in translated_audio_segments:
                    final_audio = final_audio.overlay(segment, position=start*1000)

                final_audio_path = os.path.join("/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/face_face_test/processed", "final_translated_audio.wav")
                final_audio.export(final_audio_path, format="wav")

                print("Calling remove_audio()")
                # Remove original audio from video
                silent_video_path = remove_audio(file_path)
                if not silent_video_path:
                    return 500

                if(flag == 0):
                    print("Calling merge_audio_with_silent_video()")
                    # Merge new audio with silent video
                    final_video_path = os.path.join("/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/face_face_test/processed", f"video_{utc_str}_final.mp4")
                    merge_audio_with_silent_video(silent_video_path, final_audio_path, final_video_path)
                    final_video_url = f"/processed/{os.path.basename(final_video_path)}"

                else:
                    out_name = f"result_voice_{i}.mp4"
                    subprocess.run([
                        'python3', 'inference.py',
                        '--checkpoint_path', 'checkpoints/wav2lip_gan.pth',
                        '--face', silent_video_path,
                        '--audio', final_audio_path,
                        '--wav2lip_batch_size', '128',
                        '--face_det_batch_size', '4',
                        '--output', out_name
                    ])
                    final_video_url = f"/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/results/result_voice_{i}.mp4"

                # Save the transcription to a file
                print("Saving transcription to file")
                transcription_file_path = os.path.join("/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/face_face_test/transcriptions", f"video_{utc_str}_transcription.txt")
                with open(transcription_file_path, "w") as f:
                    for line in transcription_text:
                        f.write(line + "\n")

                # Return the URL of the final video and transcription file
                transcription_file_url = f"/transcriptions/{os.path.basename(transcription_file_path)}"
            
            except Exception as r:
                return 500
                    
            #===
            
            
            
            
            split_files.append(final_video_url)
            # transcription_text.append(transcription_file_url)
        return split_files#, transcription_text
    except Exception as e:
        print(f"Error splitting video: {e}")
        return []
    




# Example usage
video_path = '/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/video.mp4'
# audio_path = '/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/video.wav'
face_intervals, no_face_intervals = detect_face_intervals(video_path)
print(f"Face Intervals: {face_intervals}")
print(f"No Face Intervals: {no_face_intervals}")

print(f"Face Merge Intervals: {merge_intervals(face_intervals)}")
print(f"No Face Merge Intervals: {merge_intervals(no_face_intervals)}")



print(split_video(video_path, merge_intervals(face_intervals), 1,'face'))
print(split_video(video_path, merge_intervals(no_face_intervals), 0,'no-face'))


#not needed
# print(split_audio(audio_path, merge_intervals(face_intervals), 'A-face'))
# print(split_audio(audio_path, merge_intervals(no_face_intervals), 'A-no-face'))









