from flask import Flask, request, jsonify
from googletrans import Translator
from gtts import gTTS
import mysql.connector
import os
import ffmpeg
from pydub import AudioSegment, silence
from moviepy.editor import VideoFileClip
import speech_recognition as sr

# from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
UPLOAD_FOLDER = 'uploads/'
PROCESSED_FOLDER = 'downloads/'
TRANSCRIPTIONS_FOLDER = 'transcriptions/'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['TRANSCRIPTIONS_FOLDER'] = TRANSCRIPTIONS_FOLDER

# app.config.from_object(Config)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'nitsilchar'
app.config['MYSQL_PASSWORD'] = 'TAR0HA=#UMF_'
app.config['MYSQL_DB'] = 'lipsync'

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="nitsilchar",
#     password="TAR0HA=#UMF_",
#     database="lipsync"
# )

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="nitsilchar",
        password="TAR0HA=#UMF_",
        database="lipsync"
)
    
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
        print(f"Conversion complete: {wav_file_path}")
        return wav_file_path
    except ffmpeg.Error as e:
        print(f"ffmpeg error: {e.stderr.decode()}")
    return None


def translate_text_file(input_text, dest_language):
    translator = Translator()
    try:
        detected_lang = translator.detect(input_text).lang
        translated = translator.translate(input_text, src=detected_lang, dest=dest_language)
        return translated.text, detected_lang
    except Exception as e:
        print(f"Error: {e}")
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
    print(f"Audio saved to {output_file_path}")
    return output_file_path

def remove_audio(input_video):
    input_stream = ffmpeg.input(input_video)
    base_name = os.path.splitext(os.path.basename(input_video))[0]
    output_video = os.path.join(PROCESSED_FOLDER, f"{base_name}_no_audio.mp4")
    output_stream = ffmpeg.output(input_stream, output_video, c='copy', an=None)
    ffmpeg.run(output_stream, overwrite_output=True)
    print(f"Output video saved to {output_video}")
    return output_video

def merge_audio_with_silent_video(silent_video, input_audio, output_video):
    input_video = ffmpeg.input(silent_video)
    input_audio = ffmpeg.input(input_audio)
    output_stream = ffmpeg.output(input_video, input_audio, output_video, vcodec='copy', acodec='aac', strict='experimental')
    ffmpeg.run(output_stream, overwrite_output=True)
    print(f"Merged video saved to {output_video}")

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
    print('12enter_hit')
    if 'video' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['video']
    print('shsss123')
    dest_lang = request.form.get('dest_lang', 'bn')  # Default to Bengali if not provided
    print('fkjn1234')
    data_usr_mail = request.form.get('u_mail_id')  # Get the user's email
    print('nwoq2212')

    # if not data_usr_mail:
    #     return jsonify({'error': 'No email provided'}), 400
    # data_usr_mail = request.data['u_mail_id']
    print(data_usr_mail)
    file_save_path = data_usr_mail + '/uploads/'
    os.makedirs(file_save_path, exist_ok=True)
    file_save_path = data_usr_mail + '/downloads/'
    os.makedirs(file_save_path, exist_ok=True)
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_save_path = data_usr_mail + '/' + file_path # data_usrmail/uploads/vid.mp4
        file.save(file_save_path)

        try:
            video = VideoFileClip(file_save_path)
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_audio.wav')
            audio_save_path = data_usr_mail + '/' + audio_path
            video.audio.write_audiofile(audio_save_path)

            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_save_path) as source:
                audio = recognizer.record(source)

            text = recognizer.recognize_google(audio)
            return jsonify({'message': 'File successfully uploaded', 'transcription': text}), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'File not allowed'}), 400



@app.route('/data', methods=['GET'])
def get_data():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS `lipsync`')
    # cursor.execute('USE `lipsync`')
    cursor.execute('CREATE TABLE IF NOT EXISTS `lipsync`.`userregdetails` (`uid` INT NOT NULL AUTO_INCREMENT , `u_fname` TEXT NOT NULL , `u_lname` TEXT NOT NULL , `u_mail` VARCHAR(90) NOT NULL , `u_pass` VARCHAR(16) NOT NULL , `u_reg_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (`uid`))')
    cursor.execute('SELECT * FROM `userregdetails`')
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(result)


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
    
    file = data['u_mail']+'/uploads'
    os.makedirs(file, exist_ok=True)
    file = data['u_mail']+'/processed'
    os.makedirs(file, exist_ok=True)

    mydb = mysql.connector.connect(host="localhost", user="nitsilchar", password="TAR0HA=#UMF_")
    db_cursor=mydb.cursor()
    db_cursor.execute('CREATE DATABASE IF NOT EXISTS lipsync')
    db_cursor.execute('USE lipsync')
    db_cursor.execute('CREATE TABLE IF NOT EXISTS lipsync.userregdetails (uid INT NOT NULL AUTO_INCREMENT , u_fname TEXT NOT NULL , u_lname TEXT NOT NULL , u_mail VARCHAR(90) NOT NULL , u_pass VARCHAR(16) NOT NULL , u_reg_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (uid))')
    query = 'INSERT INTO `userregdetails` (u_fname, u_lname, u_mail, u_pass) VALUES (%s, %s, %s, %s)'
    db_cursor.execute(query, (data['u_fname'], data['u_lname'], data['u_mail'], data['u_pass']))
    mydb.commit()
    db_cursor.execute('CREATE TABLE `lipsync`.`' + data['u_mail'] + '` (`vid` INT NOT NULL AUTO_INCREMENT , `up_vid_name` INT NOT NULL , `dwn_vid_name` INT NOT NULL , `vid_date` DATE NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (`vid`))')
    # db_cursor.execute(db_insert, ("abc", "def", "abdf@gmail.com", "1234"))
    print(db_cursor.rowcount, "Record inserted")
    return jsonify({'message': 'User created successfully'}), 123456


if __name__ == '__main__':
    app.run(debug=True, port=5000)




#file = '../file/processed/uploads'
#os.makedirs(file, exist_ok=True)