from flask import Flask, request, jsonify, send_file
import mysql.connector
import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lipsync'

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lipsync"
)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['video']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            # Extract audio from video
            video = VideoFileClip(file_path)
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_audio.wav')
            video.audio.write_audiofile(audio_path)

            # Recognize speech from audio
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)

            # Translate text to another language (e.g., Bengali)
            translator = Translator()
            translated_text = translator.translate(text, dest='bn').text

            # Convert translated text to speech
            tts = gTTS(translated_text, lang='bn')
            translated_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'translated_audio.mp3')
            tts.save(translated_audio_path)

            # Ensure translated audio is saved correctly
            if not os.path.exists(translated_audio_path):
                raise Exception("Failed to save translated audio")

            # Replace original audio with translated audio in the video
            translated_audio = VideoFileClip(translated_audio_path).audio
            final_video = video.set_audio(translated_audio)
            final_video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'translated_video.mp4')
            final_video.write_videofile(final_video_path, codec='libx264', audio_codec='aac')

            # Ensure final video is saved correctly
            if not os.path.exists(final_video_path):
                raise Exception("Failed to save final video")

            return jsonify({
                'message': 'File successfully uploaded',
                'video_url': final_video_path,
                'transcription': translated_text
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'File not allowed'}), 400

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

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS lipsync')
    cursor.execute('USE lipsync')
    cursor.execute('CREATE TABLE IF NOT EXISTS userregdetails (uid INT NOT NULL AUTO_INCREMENT , u_fname TEXT NOT NULL , u_lname TEXT NOT NULL , u_mail VARCHAR(90) NOT NULL , u_pass VARCHAR(16) NOT NULL , u_reg_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (uid))')
    query = 'INSERT INTO userregdetails (u_fname, u_lname, u_mail, u_pass) VALUES (%s, %s, %s, %s)'
    cursor.execute(query, (data['u_fname'], data['u_lname'], data['u_mail'], data['u_pass']))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'User created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
