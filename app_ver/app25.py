#=====app22.py=======


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
# import tensorflow


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
UPLOAD_FOLDER = 'upload/'
PROCESSED_FOLDER = 'processed/'
TRANSCRIPTIONS_FOLDER = 'transcriptions/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPTIONS_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['TRANSCRIPTIONS_FOLDER'] = TRANSCRIPTIONS_FOLDER

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'nitsilchar'
app.config['MYSQL_PASSWORD'] = 'TAR0HA=#UMF_'
app.config['MYSQL_DB'] = 'lipsync'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'lipsync'

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

def vid_generation():
    pad_top =  0
    pad_bottom =  15
    pad_left =  0
    pad_right =  0
    rescaleFactor =  2
    video_path = "test-1.mp4"
    video_path_fix = f"'../{video_path}'"

def detect_face_in_video(video_path):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    print("========vid captures=====")
    
    if not video_capture.isOpened():
        print("Error: Could not open video.")
        return False

    face_detected = False

    while video_capture.isOpened():
        # Read frame-by-frame
        ret, frame = video_capture.read()
        print("========while========")

        if not ret:
            break

        # Convert the image from BGR color (which OpenCV uses) to RGB color
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)

        # If faces are found, set the flag to True and break the loop
        if len(face_locations) > 0:
            face_detected = True
            break

    # Release the video capture object
    # video_capture.release()
    print(face_detected)
    return face_detected

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_text = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
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

def translate_text_file(input_text, dest_language):
    try:
        detected_lang = 'en'
        translated = GoogleTranslator(source=detected_lang, target=dest_language).translate(input_text)
        print(translated)
        return translated, detected_lang
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

def run_wav2lip(video_path, audio_path, output_path):
    # import subprocess
    result = subprocess.run(
        ['python', 'Wav2Lip/inference.py', '--checkpoint_path', 'Wav2Lip/checkpoints/wav2lip.pth',
         '--face', video_path, '--audio', audio_path, '--outfile', output_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Wav2Lip error: {result.stderr}")
        return None
    return output_path


import torch

def test_checkpoint_loading(checkpoint_path):
    try:
        checkpoint = torch.load(checkpoint_path)
        print("Checkpoint loaded successfully.")
    except Exception as e:
        print(f"Failed to load checkpoint: {e}")

# Example usage
# test_checkpoint_loading('checkpoints/wav2lip_gan.pth')

# import subprocess
# import shlex
# import torch
# import os

# def generate_video(checkpoint_path, face_video_path, audio_path, output_video_path,
#                    pad_top=0, pad_bottom=15, pad_left=0, pad_right=0, rescale_factor=2,
#                    nosmooth=True):
#     print("gen-1>>>")
#     """
#     Generate a video using the Wav2Lip model with specified parameters.

#     Args:
#     - checkpoint_path (str): Path to the Wav2Lip checkpoint file.
#     - face_video_path (str): Path to the input face video.
#     - audio_path (str): Path to the input audio file.
#     - output_video_path (str): Path to save the output video.
#     - pad_top (int): Top padding for the detection box.
#     - pad_bottom (int): Bottom padding for the detection box.
#     - pad_left (int): Left padding for the detection box.
#     - pad_right (int): Right padding for the detection box.
#     - rescale_factor (int): Rescale factor for the video.
#     - nosmooth (bool): Whether to apply smoothing to the video.

#     Returns:
#     - None
#     """
#     print("gen-2>>>")
#     try:
#         # Verify the checkpoint file path
#         if not os.path.exists(checkpoint_path):
#             print(f"Checkpoint file not found: {checkpoint_path}")
#             return

#         # Verify the face video file path
#         if not os.path.exists(face_video_path):
#             print(f"Face video file not found: {face_video_path}")
#             return

#         # Verify the audio file path
#         if not os.path.exists(audio_path):
#             print(f"Audio file not found: {audio_path}")
#             return

#         # Full path to the Python executable
#         python_executable = '/usr/bin/python3'  # Replace with the actual path to your Python executable

#         # Full path to the inference script
#         inference_script_path = 'Wav2Lip/inference.py'  # Update with the full path if necessary

#         # Prepare the command
#         command = [
#             python_executable, inference_script_path,
#             '--checkpoint_path', checkpoint_path,
#             '--face', face_video_path,
#             '--audio', audio_path,
#             '--pads', str(pad_top), str(pad_bottom), str(pad_left), str(pad_right),
#             '--resize_factor', str(rescale_factor),
#             '--outfile', output_video_path
#         ]
#         print("gen-4>>>")

#         if nosmooth:
#             print("gen-5>>>")
#             command.append('--nosmooth')
#         print("gen-6>>>")

#         # Debug: Print the command before running it
#         print(f"Running command: {' '.join(shlex.quote(arg) for arg in command)}")

#         # Execute the command
#         result = subprocess.run(command, capture_output=True, text=True)
#         print("gen-7>>>")

#         if result.returncode != 0:
#             print("gen-8>>>")
#             print(f"Error: {result.stderr}")
#         else:
#             print("gen-9>>>")
#             print(f"Output: {result.stdout}")

#     except Exception as e:
#         print("An exception occurred:")
#         print(e)

# # # Example usage
# # generate_video(
# #     checkpoint_path='checkpoints/wav2lip_gan.pth',
# #     face_video_path='processed/1_en_115202450647_final.mp4',
# #     audio_path='processed/final_translated_audio.wav',
# #     output_video_path='processed/1_en_115202450647_final_lip.mp4'
# # )

import os
import sys
sys.path.append('Wav2Lip')  # Add Wav2Lip directory to sys.path

import inference

def run_wav2lip_inference(video_path, audio_path, output_video_path,checkpoint_path='/home/oem/LIPSYNC/reactdb/client/app_ver/Wav2Lip/checkpoints/wav2lip_gan.pth', pad_top=0, pad_bottom=15, pad_left=0, pad_right=0, rescale_factor=2):
    # video_path = 'test-1.mp4',
    video_path_fix = f"'../{video_path}'"  # Adjust path accordingly if necessary
    print("1")
    inference.run(
        checkpoint_path=checkpoint_path,
        face=video_path_fix,
        audio=audio_path,
        pads=[pad_top, pad_bottom, pad_left, pad_right],
        resize_factor=rescale_factor,
        nosmooth=True,
        outfile=output_video_path
    )
    print("2")

# Example usage:


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    dest_lang = request.form.get('dest_lang', 'bn')  # Default to Bengali if not provided
    utc_str = request.form.get('utc_str')
    print("=============", utc_str, "============")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    if(detect_face_in_video(file_path)):
        detected_face = "Face Available"
    else:
        detected_face = "Face Not Available"


    transcription_text = []

    try:
        # Convert video to WAV
        audio_file_path = convert_mp4_to_wav(file_path)
        if audio_file_path is None:
            return jsonify({'error': 'Failed to convert video to audio'}), 500


        #transcription to VidUp.mjs
        # transcription = transcribe_audio(audio_file_path)


        # Load audio file
        audio = AudioSegment.from_wav(audio_file_path)
        
        # Detect non-silent regions
        non_silent_regions = detect_non_silent_regions(audio)

        translated_audio_segments = []
        for start, end in non_silent_regions:
            chunk = audio[start*1000:end*1000]  # pydub works in milliseconds
            chunk.export("chunk.wav", format="wav")

            # Transcribe the chunk
            transcription = transcribe_audio("chunk.wav")
            transcription_text.append(transcription)
            if not transcription:
                print(f"Skipping chunk {start}-{end}: Failed to transcribe audio")
                translated_audio_segments.append((start, chunk))
                continue

            # Translate the transcription
            translated_text, detected_lang = translate_text_file(transcription, dest_lang)
            if not translated_text:
                print(f"Skipping chunk {start}-{end}: Failed to translate transcription")
                translated_audio_segments.append((start, chunk))
                continue

            # Generate translated audio
            translated_audio_path = text_to_speech_from_text(translated_text, lang=dest_lang, pitch_change=0)
            translated_audio_segment = AudioSegment.from_file(translated_audio_path)
            translated_audio_segments.append((start, translated_audio_segment))

        final_audio = AudioSegment.silent(duration=len(audio))

        # Overlay translated segments back into their original positions
        for start, segment in translated_audio_segments:
            final_audio = final_audio.overlay(segment, position=start*1000)

        final_audio_path = os.path.join(PROCESSED_FOLDER, "final_translated_audio.wav")
        final_audio.export(final_audio_path, format="wav")

        # Remove original audio from video
        silent_video_path = remove_audio(file_path)
        if not silent_video_path:
            return jsonify({'error': 'Failed to remove audio from video'}), 500

        #=========

        # Merge new audio with silent video
        final_video_path_merge = os.path.join(PROCESSED_FOLDER, f"{os.path.splitext(file.filename)[0]}_{utc_str}_final.mp4")   #1 in a billion case......if same random generated for user in same time
        merge_audio_with_silent_video(silent_video_path, final_audio_path, final_video_path_merge)

        #========

        final_video_path = os.path.join(PROCESSED_FOLDER, f"{os.path.splitext(file.filename)[0]}_{utc_str}_final_lip.mp4")   #1 in a billion case......if same random generated for user in same time


        # run_wav2lip_inference(final_video_path_merge, final_audio_path, final_video_path)

        run_wav2lip_inference(final_video_path_merge, final_audio_path, final_video_path)


        # # Lipsync the silent video and the translated audio
        # final_video_path = os.path.join(PROCESSED_FOLDER, f"{os.path.splitext(file.filename)[0]}_{utc_str}_final.mp4")
        # run_wav2lip(silent_video_path, final_audio_path, final_video_path)


        # Save the transcription to a file
        transcription_file_path = os.path.join(TRANSCRIPTIONS_FOLDER, f"{os.path.splitext(file.filename)[0]}_{utc_str}_transcription.txt")
        with open(transcription_file_path, "w") as f:
            for line in transcription_text:
                f.write(line + "\n")

        # Return the URL of the final video and transcription file
        final_video_url = f"/processed/{os.path.basename(final_video_path)}"
        transcription_file_url = f"/transcriptions/{os.path.basename(transcription_file_path)}"
        
        return jsonify({
            'message': 'File successfully processed',
            'video_url': final_video_url,
            'transcription_url': transcription_file_url,
            'transcription': translated_text,  #old: transcription_text    new: translated_test
            'detected_language': detected_lang,
            'detected_face': detected_face
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        cursor.execute('SELECT * FROM demo_vids WHERE dv_sr_lang = %s and dv_dest_lang = %s', (data['u_sr_lang'], data['u_dest_lang']))
        checkFilter = cursor.fetchall()
        
        if checkFilter:
            return jsonify(checkFilter), 201
        else:
            return jsonify({'message': 'No such combination exist'}), 201
    except Error as e:
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
                    WHERE du_ip_address = %s'''
            cursor.execute(query, (data['u_sr_lang'], data['u_dest_lang'], data['u_vnum'], data['u_lip_q'], data['u_tr_q'], data['u_aud_q'], data['u_all_q'], data['u_ip_address']))
            connection.commit()
            return jsonify({'message': 'Demo user review updated successfully'}), 201
        else:
            query = '''INSERT INTO demo_usr_review 
                    (du_ip_address, du_sr_lang, du_dest_lang, du_vnum, du_lip_q, du_tr_q, du_aud_q, du_all_q) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(query, (data['u_ip_address'], data['u_sr_lang'], data['u_dest_lang'], data['u_vnum'], data['u_lip_q'], data['u_tr_q'], data['u_aud_q'], data['u_all_q']))
            connection.commit()
            return jsonify({'message': 'Demo user review submitted successfully'}), 201
    except Error as e:
        print("Error while executing SQL query", e)
        return jsonify({'error': 'Database operation failed'}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
