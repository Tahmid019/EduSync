#=====app 47========
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

import face_recognition
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.tools import subprocess_call
import ffmpeg
from pydub import AudioSegment
import numpy as np


import locale
locale.getpreferredencoding = lambda: "UTF-8"

# import locale
# locale.getpreferredencoding = lambda: "UTF-8"
#
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
UPLOAD_FOLDER = 'upload/'
PROCESSED_FOLDER = 'processed/'
RESULTS = 'results/'
TRANSCRIPTIONS_FOLDER = 'transcriptions/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPTIONS_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['TRANSCRIPTIONS_FOLDER'] = TRANSCRIPTIONS_FOLDER
app.config['RESULTS'] = RESULTS


# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'nitsilchar'
app.config['MYSQL_PASSWORD'] = 'TAR0HA=#UMF_'
app.config['MYSQL_DB'] = 'lipsync'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'lipsync'

# Absolute or relative path to the external directory
VIDEO_DIRECTORY = '/Wav2Lip/processed'

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
        wav_file_path = os.path.join(PROCESSED_FOLDER, f"{base_name}.wav")
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
    temp_audio_path = os.path.join(PROCESSED_FOLDER, "temp_output.mp3")
    tts.save(temp_audio_path)

    audio = AudioSegment.from_file(temp_audio_path)
    audio = audio + amplitude_change

    if pitch_change != 0:
        new_sample_rate = int(audio.frame_rate * (2.0 ** (pitch_change / 12.0)))
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
        audio = audio.set_frame_rate(44100)

    output_file_path = os.path.join(PROCESSED_FOLDER, "translated_output.mp3")
    audio.export(output_file_path, format="mp3")
    return output_file_path

def remove_audio(input_video):
    input_stream = ffmpeg.input(input_video)
    base_name = os.path.splitext(os.path.basename(input_video))[0]
    output_video = os.path.join(PROCESSED_FOLDER, f"{base_name}_no_audio.mp4")
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
    
    duration = clip.duration
    face_detected = None
    start_time = 0

    # Smooth the frame processing by using a buffer
    buffer_size = 7
    buffer = []

    def process_frame(frame, t):
        nonlocal face_detected, start_time, buffer
        current_time = t

        # Convert frame to RGB
        rgb_frame = frame[:, :, ::-1]
        
        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        
        buffer.append(len(face_locations) > 0)
        if len(buffer) > buffer_size:
            buffer.pop(0)

        # Check if face is consistently detected in the buffer
        if np.mean(buffer) > 0.25:
            detected = True
        else:
            detected = False

        if detected:
            if face_detected is False or face_detected is None:
                # Append interval for no-face region
                if face_detected is False:
                    face_intervals.append((start_time, current_time - start_time, 0))
                # Update start time
                start_time = current_time
                face_detected = True
        else:
            if face_detected is True or face_detected is None:
                # Append interval for face region
                if face_detected is True:
                    face_intervals.append((start_time, current_time - start_time, 1))
                # Update start time
                start_time = current_time
                face_detected = False
    
    # Process the video frame by frame
    for t, frame in clip.iter_frames(fps=1, with_times=True, dtype='uint8'):
        process_frame(frame, t)

    # Finalize intervals
    if face_detected is not None:
        face_intervals.append((start_time, duration - start_time, 1 if face_detected else 0))

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
  
def split_audio(audio_path, face_intervals, output_prefix):
    audio = AudioSegment.from_wav(audio_path)
    split_files = []
    for i, (start, duration, value) in enumerate(face_intervals):
        output_path = f"{output_prefix}_fiv-{value}_{i}.wav"
        end = start + duration
        chunk = audio[start*1000:end*1000]  # pydub works in milliseconds
        chunk.export(output_path, format="wav")
        split_files.append(output_path)
    return split_files
  
def up_f(file_path, sr_lang, dest_lang, utc_str, flag):

    # file_path = os.path.join(UPLOAD_FOLDER, file_path)
    print("=================")
    print("=================")
    print("=================")
    print(file_path)
    print(flag)
    print("=================")
    print("=================")
    print("=================")

    transcription_text = []

    try:
        # Convert video to WAV
        print("Calling convert_mp4_to_wav()")
        audio_file_path = convert_mp4_to_wav(file_path)
        if audio_file_path is None:
            return jsonify({'error': 'Failed to convert video to audio'}), 500

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
            translated_audio_segment = AudioSegment.from_file(translated_audio_path)
            translated_audio_segments.append((start, translated_audio_segment))

        final_audio = AudioSegment.silent(duration=len(audio))

        # Overlay translated segments back into their original positions
        for start, segment in translated_audio_segments:
            final_audio = final_audio.overlay(segment, position=start*1000)

        final_audio_path = os.path.join(PROCESSED_FOLDER, "final_translated_audio.wav")
        final_audio.export(final_audio_path, format="wav")

        print("Calling remove_audio()")
        # Remove original audio from video
        silent_video_path = remove_audio(file_path)
        if not silent_video_path:
            return jsonify({'error': 'Failed to remove audio from video'}), 500

        
        final_video_path = os.path.join(PROCESSED_FOLDER, f"{os.path.splitext(file_path)[0]}_{utc_str}_final.mp4")

        if flag==0:
            try:
                print("Calling merge_audio_with_silent_video()")
                # Merge new audio with silent video
                merge_audio_with_silent_video(silent_video_path, final_audio_path, final_video_path)
            except Exception as merge_error:
                print(f"[[Error]]: {merge_error}")
        else: 
            try: 
                
                print("Calling Subprocess ....")
                subprocess.run([
                    'python3', 'inference.py',
                    '--checkpoint_path', 'checkpoints/wav2lip_gan.pth',
                    '--face', silent_video_path,
                    
                    '--audio', final_audio_path,
                    '--face_det_batch_size', '1',
                    '--wav2lip_batch_size', '1',
                    '--outfile', final_video_path
                ])
                while(True):
                    if (find_file(PROCESSED_FOLDER, f"{os.path.splitext(file_path)[0]}_{utc_str}_final.mp4")):
                        print("FOUND")
                        break
                    print("NOT FOUND")
                    time.sleep(600)
                    continue
            except Exception as subprocess_er:
                print(f"[[Error]]: {subprocess_er}")
                
        # Save the transcription to a file
        print("Saving transcription to file")
        transcription_file_path = os.path.join(TRANSCRIPTIONS_FOLDER, f"{os.path.splitext(file_path)[0]}_{utc_str}_transcription.txt")
        with open(transcription_file_path, "w") as f:
            for line in transcription_text:
                f.write(line + "\n")

        # Return the URL of the final video and transcription file
        final_video_url = f"/processed/{os.path.basename(final_video_path)}"
        transcription_file_url = f"/transcriptions/{os.path.basename(transcription_file_path)}"
        
        return final_video_url, transcription_file_url
    except Exception as up:
        print(f"[ ERROR ]: {up}")
        return []

def find_file(directory, filename):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            print(f"[[==>{os.path.join(root, filename)}<=== ]]")
            return True
    return False

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



@app.route('/upload', methods=['POST'])
def upload_file():
    # print("=======sleep for 3*60")
    # time.sleep(3*60)
    # print("=======sleep over...")
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 4001

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 4002

    print("=======file uploaded...")
    sr_lang = request.form.get('sr_lang')
    dest_lang = request.form.get('dest_lang', 'bn')
    utc_str = request.form.get('utc_str')
    
    print("=======try...")
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
    except Exception as e:
        return jsonify({'error': f'Failed to save file: {str(e)}'}), 5001

    try:
        # Face detection and merging intervals
        print("=======face detect...")
        face_intervals = detect_face_intervals(file_path)
        print(face_intervals)
        print("=======calling merge...")
        merge = merge_intervals(face_intervals)
        print(merge)
        num_seg = len(merge)
        print(num_seg)
        
        

        # Convert video to audio
        print("=======calling con mp4 to wav...")
        audio_file_path = convert_mp4_to_wav(file_path)
        if audio_file_path is None:
            return jsonify({'error': 'Failed to convert video to audio'}), 5002

        # Detect non-silent regions
        print("=======calling silent reg...")
        audio = AudioSegment.from_wav(audio_file_path)
        non_silent_regions = detect_non_silent_regions(audio)

        translated_audio_segments = []
        transcription_text = []

        print("=======calling loop for silent det...")
        for start, end in non_silent_regions:
            chunk = audio[start*1000:end*1000]
            chunk.export("chunk.wav", format="wav")

            transcription = transcribe_audio("chunk.wav", sr_lang)
            transcription_text.append(transcription)
            if not transcription:
                print("not transcription =======")
                continue

            translated_text, detected_lang = translate_text_file(transcription, dest_lang, sr_lang)
            if not translated_text:
                print("not translated=======")
                continue

            translated_audio_path = text_to_speech_from_text(translated_text, lang=dest_lang, pitch_change=0)
            translated_audio_segment = AudioSegment.from_file(translated_audio_path)
            translated_audio_segments.append((start, translated_audio_segment))

        final_audio = AudioSegment.silent(duration=len(audio))
        print("=======calling overly...")
        for start, segment in translated_audio_segments:
            final_audio = final_audio.overlay(segment, position=start*1000)

        final_audio_path = os.path.join(PROCESSED_FOLDER, f"trans_{utc_str}.wav")
        final_audio.export(final_audio_path, format="wav")

        silent_video_path = remove_audio(file_path)
        if not silent_video_path:
            return jsonify({'error': 'Failed to remove audio from video'}), 5003

        print("=======calling split vid...")
        vid_chunks = split_video(silent_video_path, merge, f"vidChunk_{utc_str}")
        print("=======calling split aud...")
        aud_chunks = split_audio(final_audio_path, merge, f"audChunk_{utc_str}")

        final = []
        print("=======caling seg loop...")
        for i in range(0,num_seg):
            print(f"Merge: {merge}")
            chunk = os.path.join(PROCESSED_FOLDER, f"chunk_{i}_{utc_str}.mp4")
            print("=======if_else....")
            if merge[i][2] == 1:
                print("=======try subprocess...")
                subprocess.run([
                    'python3', 'inference.py',
                    '--checkpoint_path', 'checkpoints/wav2lip_gan.pth',
                    '--face', vid_chunks[i],
                    '--audio', aud_chunks[i],
                    '--face_det_batch_size', '2',
                    '--outfile', chunk
                ], check=True)
                final.append(chunk)
                print("=======subprocess over...")
                print(f"[{i}] == > {chunk}  || {final}")
                # try:
                #     subprocess.run([
                #         'python3', 'inference.py',
                #         '--checkpoint_path', 'checkpoints/wav2lip_gan.pth',
                #         '--face', vid_chunks[i],
                #         '--audio', aud_chunks[i],
                #         '--face_det_batch_size', '1',
                #         '--outfile', chunk
                #     ], check=True)
                #     final.append(chunk)
                # except Exception as subprocess_err:
                #     merge_audio_with_silent_video(vid_chunks[i], aud_chunks[i], chunk)
                #     final.append(chunk)
                # print("=======sleep 3*60")
                # # time.sleep(3*60)
                # print("=======sleep over...")
            else:
                print("=======Calling Merge...")
                merge_audio_with_silent_video(vid_chunks[i], aud_chunks[i], chunk)
                final.append(chunk)
                print(final)
                print("=======Merge over...")
        # final_video_path = os.path.join(f"{utc_str}.mp4")
                
        final_video = process_videos(final, PROCESSED_FOLDER, utc_str)
        print(final_video)
        
        final_video_path = os.path.join(f'{os.path.basename(final_video)}')
        print(final_video_path)
    
        
        print("6")
        print(final_video_path)
        print(translated_text)
        
        
        transcription_file_path = os.path.join(TRANSCRIPTIONS_FOLDER, f"{utc_str}_transcription.txt")
        with open(transcription_file_path, "w") as f:
            for line in transcription_text:
                f.write(line + "\n")

        return jsonify({
            'message': 'File successfully processed',
            'video_url': f"/processed/{final_video_path}",
            'transcription_url': transcription_file_path,
            'transcription': transcription_text
        }), 2001

    except Exception as e:
        return jsonify({'error': str(e)}), 5004
    
@app.route('/video/<filename>')
def serve_video(filename):
    return send_from_directory(os.getcwd(), filename)
    
@app.route('/transcriptions/<filename>')
def serve_transcription_file(filename):
    return send_from_directory(TRANSCRIPTIONS_FOLDER, filename)

@app.route('/data', methods=['GET'])
def get_data():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS `lipsync`')
    cursor.execute('CREATE TABLE IF NOT EXISTS `lipsync`.`userregdetails` (`uid` INT NOT NULL AUTO_INCREMENT , `u_fname` TEXT NOT NULL , `u_lname` TEXT NOT NULL , `u_mail` VARCHAR(90) NOT NULL , `u_pwd` VARCHAR(20) NOT NULL , PRIMARY KEY (`uid`), UNIQUE(`u_mail`))')
    cursor.execute('SELECT * FROM `userregdetails`')
    data = cursor.fetchall()
    connection.close()
    return jsonify(data)

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/results/<filename>')
def results_file(filename):
    return send_from_directory(app.config['RESULTS'], filename)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

@app.route('/user', methods=['POST'])
def signup():
    print("test")
    # return jsonify("test1")
    data = request.get_json()
    print('Received data:', data) # Log received data

    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
        
    required_fields = ['u_fname', 'u_lname', 'u_mail', 'u_pass']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    mydb = mysql.connector.connect(host="localhost", user="nitsilchar", password="TAR0HA=#UMF_")
    # mydb = mysql.connector.connect(host="localhost", user="root", password="")
    db_cursor=mydb.cursor()
    db_cursor.execute('CREATE DATABASE IF NOT EXISTS lipsync')
    db_cursor.execute('USE lipsync')
    db_cursor.execute('CREATE TABLE IF NOT EXISTS lipsync.userregdetails (uid INT NOT NULL AUTO_INCREMENT , u_fname TEXT NOT NULL , u_lname TEXT NOT NULL , u_mail VARCHAR(90) NOT NULL , u_pass VARCHAR(16) NOT NULL , u_reg_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (uid))')
    query = 'INSERT INTO `userregdetails` (u_fname, u_lname, u_mail, u_pass) VALUES (%s, %s, %s, %s)'
    db_cursor.execute(query, (data['u_fname'], data['u_lname'], data['u_mail'], data['u_pass']))
    # db_cursor.execute(db_insert, ("abc", "def", "abdf@gmail.com", "1234"))
    mydb.commit()
    print(db_cursor.rowcount, "Record inserted")
    return jsonify({'message': 'User created successfully'}), 123456

@app.route('/demofilter', methods=['POST'])
def demofilter():
    data = request.get_json()
    print('Received data:', data) 

    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    required_fields = ['u_sr_lang', 'u_dest_lang']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS lipsync')
        cursor.execute('USE lipsync')
        cursor.execute('SELECT * FROM `demo_usr_review` RIGHT OUTER JOIN `demo_vids` ON `demo_usr_review`.`du_vnum` = `demo_vids`.`dvnum` WHERE `demo_vids`.`dv_sr_lang` = %s AND `demo_vids`.`dv_dest_lang` = %s; ', (data['u_sr_lang'], data['u_dest_lang']))
        checkFilter = cursor.fetchall()
        print(checkFilter)
        
        if checkFilter:
            return jsonify(checkFilter), 201
        else:
            return jsonify({'message': 'No such combination exist'}), 201
    except Exception as e:
        print("Error while executing SQL query", e)
        return jsonify({'error': 'Database operation failed'}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return 0

@app.route('/demouser', methods=['POST'])
def demouser():
    data = request.get_json()
    print('Received data:', data)  # Log received data

    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    required_fields = ['u_ip_address', 'u_sr_lang', 'u_dest_lang', 'u_vnum', 'u_lip_q', 'u_tr_q', 'u_aud_q', 'u_all_q']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS lipsync')
        cursor.execute('USE lipsync')
        cursor.execute('''CREATE TABLE IF NOT EXISTS demo_usr_review (
                            duid INT NOT NULL AUTO_INCREMENT,
                            du_ip_address VARCHAR(100) NOT NULL,
                            du_sr_lang TEXT NOT NULL,
                            du_dest_lang TEXT NOT NULL,
                            du_vnum INT NOT NULL,
                            du_lip_q INT NOT NULL,
                            du_tr_q INT NOT NULL,
                            du_aud_q INT NOT NULL,
                            du_all_q INT NOT NULL,
                            du_review_timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                            PRIMARY KEY (duid)
                        )''')
        cursor.execute('SELECT * FROM demo_usr_review WHERE du_ip_address = %s and du_vnum = %s', (data['u_ip_address'], data['u_vnum']))
        checkIp = cursor.fetchone()
        
        if checkIp:
            query = '''UPDATE demo_usr_review SET
                    du_sr_lang = %s, du_dest_lang = %s, du_vnum = %s, du_lip_q = %s, du_tr_q = %s, du_aud_q = %s, du_all_q = %s
                    WHERE du_ip_address = %s and du_vnum = %s'''
            cursor.execute(query, (data['u_sr_lang'], data['u_dest_lang'], data['u_vnum'], data['u_lip_q'], data['u_tr_q'], data['u_aud_q'], data['u_all_q'], data['u_ip_address'], data['u_vnum']))
            connection.commit()
            return jsonify({'message': 'Demo user review updated successfully'}), 201
        else:
            query = '''INSERT INTO demo_usr_review 
                    (du_ip_address, du_sr_lang, du_dest_lang, du_vnum, du_lip_q, du_tr_q, du_aud_q, du_all_q) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(query, (data['u_ip_address'], data['u_sr_lang'], data['u_dest_lang'], data['u_vnum'], data['u_lip_q'], data['u_tr_q'], data['u_aud_q'], data['u_all_q']))
            connection.commit()
            return jsonify({'message': 'Demo user review submitted successfully'}), 201
    except Exception as e:
        print("Error while executing SQL query", e)
        return jsonify({'error': 'Database operation failed'}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/check-file', methods=['GET'])
def check_file():
    print(f"[[==>{request.args.get('filename')}<=== ]]")
    filename = request.args.get('filename')
    file_path = os.path.join(VIDEO_DIRECTORY, filename)
    if os.path.exists(file_path):
        print(f"File exists: {file_path}")
        return jsonify({"exists": True}), 200
    else:
        print(f"File does not exist: {file_path}")
        return jsonify({"exists": False}), 404


@app.route('/uploads/<filename>', methods=['GET'])
def serve_file(filename):
    print(f"[[==>{filename}<=== ]]")
    return send_from_directory(VIDEO_DIRECTORY, filename)



if __name__ == '__main__':
    app.run(debug=True, port=5000)

