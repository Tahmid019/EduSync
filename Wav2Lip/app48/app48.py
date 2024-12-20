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

from routes.audio import audio_bp
from routes.translation import translation_bp

from database.connection import get_db_connection
from utils.audio_processes import transcribe_audio, text_to_speech_from_text, detect_non_silent_regions, split_audio
from utils.text_processes import detect_language, translate_text_file
from utils.video_processes  import remove_audio, process_frame, process_videos, split_video, detect_face_intervals
from utils.helpers import convert_mp4_to_wav, merge_audio_with_silent_video, save_file, find_file, merge_intervals

import locale
locale.getpreferredencoding = lambda: "UTF-8"

app = Flask(__name__)
CORS(app)

#load configuration
app.config.from_pyfile('config/settings.py')

#creating required directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
os.makedirs(app.config['TRANSCRIPTIONS_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS'], exist_ok=True)

#global variables
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
PROCESSED_FOLDER = app.config['PROCESSED_FOLDER']
TRANSCRIPTIONS_FOLDER = app.config['TRANSCRIPTIONS_FOLDER']
RESULTS = app.config['RESULTS']

#register blueprints
app.register_blueprint(audio_bp, url_prefix='/api/audio')
app.register_blueprint(translation_bp, url_prefix='/api/translation')

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), '../Wav2Lip/inference.py'))
INFERENCE_SCRIPT = os.path.join(BASE_DIR, 'inference.py')
CHECKPOINT_PATH = os.path.join(BASE_DIR, 'checkpoints', 'wav2lip_gan.pth')



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
        audio_file_path = convert_mp4_to_wav(file_path, PROCESSED_FOLDER)
        if audio_file_path is None:
            return jsonify({'error': 'Failed to convert video to audio'}), 5002

        # Detect non-silent regions
        print("=======calling silent reg...")
        print(1)
        audio = AudioSegment.from_wav(audio_file_path)
        print(2)
        non_silent_regions = detect_non_silent_regions(audio)
        print(3)
        translated_audio_segments = []
        transcription_text = []
        print(f"non silent regions: {non_silent_regions}")

        print("=======calling loop for silent det...")
        print(non_silent_regions)
        for start, end in non_silent_regions:
            print(f"start: {start}, end: {end}")
            chunk = audio[start*1000:end*1000]
            print("===in loop====calling export wav...")
            chunk.export("chunk.wav", format="wav")
            
            print("===in loop====calling transcribe audio...")
            transcription = transcribe_audio("chunk.wav", sr_lang)
            transcription_text.append(transcription)
            if not transcription:
                print("not transcription =======")
                continue

            translated_text, detected_lang = translate_text_file(transcription, dest_lang, sr_lang)
            if not translated_text:
                print("not translated=======")
                continue

            translated_audio_path = text_to_speech_from_text(PROCESSED_FOLDER, translated_text, lang=dest_lang, pitch_change=0)
            translated_audio_segment = AudioSegment.from_file(translated_audio_path)
            translated_audio_segments.append((start, translated_audio_segment))

        final_audio = AudioSegment.silent(duration=len(audio))
        print("=======calling overly...")
        for start, segment in translated_audio_segments:
            final_audio = final_audio.overlay(segment, position=start*1000)

        final_audio_path = os.path.join(PROCESSED_FOLDER, f"trans_{utc_str}.wav")
        final_audio.export(final_audio_path, format="wav")

        silent_video_path = remove_audio(file_path, PROCESSED_FOLDER)
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
                    'python3', INFERENCE_SCRIPT,
                    '--checkpoint_path', CHECKPOINT_PATH,
                    '--face', vid_chunks[i],
                    '--audio', aud_chunks[i],
                    '--face_det_batch_size', '16',
                    '--outfile', chunk
                ], check=True)
                final.append(chunk)
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



if __name__ == "__main__":
    app.run(debug=True)
