from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
import os
import speech_recognition as sr
import ffmpeg
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment, silence
from moviepy.editor import VideoFileClip
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Setup logging
logging.basicConfig(level=logging.INFO)

# Define folder paths
UPLOAD_FOLDER = 'uploads/'
PROCESSED_FOLDER = 'downloads/'
TRANSCRIPTIONS_FOLDER = 'transcriptions/'
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

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_text = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_text)
        return text
    except sr.UnknownValueError:
        logging.error("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        logging.error(f"Could not request results from Google Speech Recognition service; {e}")
    return ""

def convert_mp4_to_wav(mp4_file_path, data_mail_id):
    try:
        base_name = os.path.splitext(os.path.basename(mp4_file_path))[0]
        user_folder = os.path.join(data_mail_id, PROCESSED_FOLDER)
        os.makedirs(user_folder, exist_ok=True)
        wav_file_path = os.path.join(user_folder, f"{base_name}.wav")
        ffmpeg.input(mp4_file_path).output(wav_file_path, format='wav').run(overwrite_output=True)
        logging.info(f"Conversion complete: {wav_file_path}")
        return wav_file_path
    except ffmpeg.Error as e:
        logging.error(f"ffmpeg error: {e.stderr.decode()}")
    return None

def translate_text_file(input_text, dest_language):
    translator = Translator()
    try:
        detected_lang = translator.detect(input_text).lang
        translated = translator.translate(input_text, src=detected_lang, dest=dest_language)
        return translated.text, detected_lang
    except Exception as e:
        logging.error(f"Error: {e}")
    return "", ""

def text_to_speech_from_text(data_mail_id, text, lang='bn', amplitude_change=0, pitch_change=0):
    tts = gTTS(text=text, lang=lang)
    user_folder = os.path.join(data_mail_id, PROCESSED_FOLDER)
    os.makedirs(user_folder, exist_ok=True)
    temp_audio_path = os.path.join(user_folder, "temp_output.mp3")
    tts.save(temp_audio_path)

    audio = AudioSegment.from_file(temp_audio_path)
    audio = audio + amplitude_change

    if pitch_change != 0:
        new_sample_rate = int(audio.frame_rate * (2.0 ** (pitch_change / 12.0)))
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
        audio = audio.set_frame_rate(44100)

    output_file_path = os.path.join(user_folder, "translated_output.mp3")
    audio.export(output_file_path, format="mp3")
    logging.info(f"Audio saved to {output_file_path}")
    return output_file_path

def remove_audio(data_mail_id, input_video):
    try:
        input_stream = ffmpeg.input(input_video)
        base_name = os.path.splitext(os.path.basename(input_video))[0]
        user_folder = os.path.join(data_mail_id, PROCESSED_FOLDER)
        os.makedirs(user_folder, exist_ok=True)
        output_video = os.path.join(user_folder, f"{base_name}_no_audio.mp4")
        ffmpeg.output(input_stream, output_video, c='copy', an=None).run(overwrite_output=True)
        logging.info(f"Output video saved to {output_video}")
        return output_video
    except ffmpeg.Error as e:
        logging.error(f"ffmpeg error: {e.stderr.decode()}")
    return None

def merge_audio_with_silent_video(silent_video, input_audio, output_video):
    try:
        input_video = ffmpeg.input(silent_video)
        input_audio = ffmpeg.input(input_audio)
        ffmpeg.output(input_video, input_audio, output_video, vcodec='copy', acodec='aac', strict='experimental').run(overwrite_output=True)
        logging.info(f"Merged video saved to {output_video}")
    except ffmpeg.Error as e:
        logging.error(f"ffmpeg error: {e.stderr.decode()}")

def detect_non_silent_regions(audio, silence_thresh=-70, min_silence_len=1000):
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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['video']
    dest_lang = request.form.get('dest_lang', 'bn')  # Default to Bengali if not provided
    data_usr_mail = request.form.get('u_mail_id')  # Get the user's email

    if not data_usr_mail:
        return jsonify({'error': 'No email provided'}), 400
    
    user_folder = os.path.join(data_usr_mail, UPLOAD_FOLDER)
    os.makedirs(user_folder, exist_ok=True)
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file:
        filename = file.filename
        file_path = os.path.join(user_folder, filename)
        file.save(file_path)
        
        transcription_text = []

        try:
            audio_file_path = convert_mp4_to_wav(file_path, data_usr_mail)
            if audio_file_path is None:
                return jsonify({'error': 'Failed to convert video to audio'}), 500

            audio = AudioSegment.from_wav(audio_file_path)
            non_silent_regions = detect_non_silent_regions(audio)
            
            translated_audio_segments = []
            for start, end in non_silent_regions:
                chunk = audio[start*1000:end*1000]  # pydub works in milliseconds
                chunk.export("chunk.wav", format="wav")

                transcription = transcribe_audio("chunk.wav")
                transcription_text.append(transcription)
                if not transcription:
                    logging.warning(f"Skipping chunk {start}-{end}: Failed to transcribe audio")
                    translated_audio_segments.append((start, chunk))
                    continue
                
                translated_text, detected_lang = translate_text_file(transcription, dest_lang)
                if not translated_text:
                    logging.warning(f"Skipping chunk {start}-{end}: Failed to translate transcription")
                    translated_audio_segments.append((start, chunk))
                    continue
                
                translated_audio_path = text_to_speech_from_text(data_usr_mail, translated_text, lang=dest_lang, pitch_change=0)
                translated_audio_segment = AudioSegment.from_file(translated_audio_path)
                translated_audio_segments.append((start, translated_audio_segment))
                
            final_audio = AudioSegment.silent(duration=len(audio))
            for start, segment in translated_audio_segments:
                final_audio = final_audio.overlay(segment, position=start*1000)

            final_audio_path = os.path.join(user_folder, "final_translated_audio.wav")
            final_audio.export(final_audio_path, format="wav")
            
            silent_video_path = remove_audio(data_usr_mail, file_path)
            if not silent_video_path:
                return jsonify({'error': 'Failed to remove audio from video'}), 500

            final_video_path = os.path.join(user_folder, f"{os.path.splitext(file.filename)[0]}_final.mp4")
            merge_audio_with_silent_video(silent_video_path, final_audio_path, final_video_path)

            transcription_file_path = os.path.join(data_usr_mail, TRANSCRIPTIONS_FOLDER, f"{os.path.splitext(file.filename)[0]}_transcription.txt")
            os.makedirs(os.path.dirname(transcription_file_path), exist_ok=True)
            with open(transcription_file_path, "w") as f:
                for line in transcription_text:
                    f.write(line + "\n")
                    
            final_video_url = f"/{data_usr_mail}/downloads/{os.path.basename(final_video_path)}"
            transcription_file_url = f"/{data_usr_mail}/transcriptions/{os.path.basename(transcription_file_path)}"
            return jsonify({
                'message': 'File successfully processed',
                'video_url': final_video_url,
                'transcription_url': transcription_file_url,
                'transcription': transcription_text,
                'detected_language': detected_lang
            }), 200
        
        except Exception as e:
            logging.error(f"Exception: {str(e)}")
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'File not allowed'}), 400

@app.route('/transcriptions/<filename>')
def serve_transcription_file(filename):
    return send_from_directory(TRANSCRIPTIONS_FOLDER, filename)

@app.route('/data', methods=['GET'])
def get_data():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS `lipsync`')
    cursor.execute('CREATE TABLE IF NOT EXISTS `lipsync`.`userregdetails` (`uid` INT NOT NULL AUTO_INCREMENT , `u_fname` TEXT NOT NULL , `u_lname` TEXT NOT NULL , `u_mail` VARCHAR(90) NOT NULL , `u_pass` VARCHAR(16) NOT NULL , `u_reg_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (`uid`))')
    cursor.execute('SELECT * FROM `userregdetails`')
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(result)

@app.route('/user', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
        
    required_fields = ['u_fname', 'u_lname', 'u_mail', 'u_pass']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    user_folder = os.path.join(data['u_mail'], 'uploads')
    os.makedirs(user_folder, exist_ok=True)
    processed_folder = os.path.join(data['u_mail'], 'processed')
    os.makedirs(processed_folder, exist_ok=True)

    mydb = get_db_connection()
    db_cursor = mydb.cursor()
    db_cursor.execute('CREATE DATABASE IF NOT EXISTS lipsync')
    db_cursor.execute('USE lipsync')
    db_cursor.execute('CREATE TABLE IF NOT EXISTS lipsync.userregdetails (uid INT NOT NULL AUTO_INCREMENT , u_fname TEXT NOT NULL , u_lname TEXT NOT NULL , u_mail VARCHAR(90) NOT NULL , u_pass VARCHAR(16) NOT NULL , u_reg_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (uid))')
    query = 'INSERT INTO userregdetails (u_fname, u_lname, u_mail, u_pass) VALUES (%s, %s, %s, %s)'
    db_cursor.execute(query, (data['u_fname'], data['u_lname'], data['u_mail'], data['u_pass']))
    mydb.commit()
    db_cursor.execute(f'CREATE TABLE IF NOT EXISTS `{data["u_mail"]}` (vid INT NOT NULL AUTO_INCREMENT , up_vid_name INT NOT NULL , dwn_vid_name INT NOT NULL , vid_date DATE NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (vid))')
    db_cursor.close()
    mydb.close()
    return jsonify({'message': 'User created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
