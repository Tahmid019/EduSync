from deep_translator import GoogleTranslator
from flask import Flask, request, jsonify, send_from_directory
import os
import speech_recognition as sr
import ffmpeg
from gtts import gTTS
from pydub import AudioSegment, silence
from flask_cors import CORS
import mysql.connector
import face_recognition
import cv2
import subprocess

import locale
locale.getpreferredencoding = lambda: "UTF-8"

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

def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

def run_wav2lip(face_video_path, audio_path, output_path, 
                checkpoint_path='checkpoints/wav2lip_gan.pth', 
                pad_top=0, pad_bottom=15, pad_left=0, pad_right=0, rescale_factor=2):
    command = [
        'python', 'Wav2Lip/inference.py',
        '--checkpoint_path', checkpoint_path,
        '--face', face_video_path,
        '--audio', audio_path,
        '--pads', str(pad_top), str(pad_bottom), str(pad_left), str(pad_right),
        '--resize_factor', str(rescale_factor),
        '--nosmooth',
        '--outfile', output_path
    ]
    subprocess.run(command, check=True)

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

    if detect_face_in_video(file_path):
        detected_face = "Face Available"
    else:
        detected_face = "Face Not Available"

    transcription_text = []

    try:
        # Convert video to WAV
        audio_file_path = convert_mp4_to_wav(file_path)
        if audio_file_path is None:
            return jsonify({'error': 'Failed to convert video to audio'}), 500

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

        # Merge new audio with silent video
        final_video_path = os.path.join(PROCESSED_FOLDER, f"{os.path.splitext(file.filename)[0]}_{utc_str}_final.mp4")   #1 in a billion case......if same random generated for user in same time
        merge_audio_with_silent_video(silent_video_path, final_audio_path, final_video_path)

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
            'transcription': translated_text,  # old: transcription_text, new: translated_text
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
    data = request.get_json()
    print('Received data:', data)  # Log received data

    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    required_fields = ['u_fname', 'u_lname', 'u_mail', 'u_pass']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS lipsync')
    cursor.execute('USE lipsync')
    cursor.execute('CREATE TABLE IF NOT EXISTS lipsync.userregdetails (uid INT NOT NULL AUTO_INCREMENT , u_fname TEXT NOT NULL , u_lname TEXT NOT NULL , u_mail VARCHAR(90) NOT NULL , u_pass VARCHAR(16) NOT NULL , u_reg_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (uid))')
    query = 'INSERT INTO userregdetails (u_fname, u_lname, u_mail, u_pass) VALUES (%s, %s, %s, %s)'
    cursor.execute(query, (data['u_fname'], data['u_lname'], data['u_mail'], data['u_pass']))
    connection.commit()
    connection.close()
    return jsonify({'message': 'User created successfully'}), 201

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

def convert_mp4_to_wav(video_path):
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    try:
        ffmpeg.input(video_path).output(audio_path).run()
        return audio_path
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e}")
        return None

def detect_non_silent_regions(audio, min_silence_len=1000, silence_thresh=-80):
    non_silent_ranges = silence.detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    non_silent_ranges_sec = [(start / 1000, end / 1000) for start, end in non_silent_ranges]
    return non_silent_ranges_sec

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None

def translate_text_file(text, dest_lang):
    try:
        translated_text = GoogleTranslator(source='auto', target=dest_lang).translate(text)
        detected_lang = GoogleTranslator(source='auto', target=dest_lang).detect(text)
        return translated_text, detected_lang
    except Exception as e:
        print(f"Translation error: {e}")
        return None, None

def text_to_speech_from_text(text, lang='en', pitch_change=0):
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_path = "translated_audio.mp3"
    tts.save(audio_path)
    return audio_path

def remove_audio(video_path):
    silent_video_path = video_path.rsplit('.', 1)[0] + '_silent.mp4'
    try:
        ffmpeg.input(video_path).output(silent_video_path, vcodec='copy', an=None).run()
        return silent_video_path
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e}")
        return None


def merge_audio_with_silent_video(silent_video, input_audio, output_video):
    input_video = ffmpeg.input(silent_video)
    input_audio = ffmpeg.input(input_audio)
    output_stream = ffmpeg.output(input_video, input_audio, output_video, vcodec='copy', acodec='aac', strict='experimental')
    ffmpeg.run(output_stream, overwrite_output=True)


def detect_face_in_video(video_path):
    video = cv2.VideoCapture(video_path)
    face_detected = False

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        if face_locations:
            face_detected = True
            break

    video.release()
    return face_detected

def run_wav2lip(video_path, audio_path, output_path):
    import subprocess
    result = subprocess.run(
        ['python', 'Wav2Lip/inference.py', '--checkpoint_path', 'Wav2Lip/checkpoints/wav2lip.pth',
         '--face', video_path, '--audio', audio_path, '--outfile', output_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Wav2Lip error: {result.stderr}")
        return None
    return output_path

if __name__ == '__main__':
    app.run(debug=True, port=5000)
