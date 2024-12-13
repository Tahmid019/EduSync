from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
import os
import speech_recognition as sr
import ffmpeg
# from googletrans import Translator
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment, silence
from moviepy.editor import VideoFileClip

# from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
UPLOAD_FOLDER = 'upload/'
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


def convert_mp4_to_wav(mp4_file_path, data_mail_id):
    try:
        base_name = os.path.splitext(os.path.basename(mp4_file_path))[0]
        wav_file_path = os.path.join(PROCESSED_FOLDER, f"{base_name}.wav")
        wav_file_final_path = data_mail_id + '/' + wav_file_path
        ffmpeg.input(mp4_file_path).output(wav_file_final_path, format='wav').run(overwrite_output=True)
        print(f"Conversion complete: {wav_file_final_path}")
        return wav_file_final_path
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

def text_to_speech_from_text(data_mail_id, text, lang='bn', amplitude_change=0, pitch_change=0):
    tts = gTTS(text=text, lang=lang)
    temp_audio_path = os.path.join(PROCESSED_FOLDER, "temp_output.mp3")
    temp_audio_final_path = data_mail_id + '/' + temp_audio_path
    tts.save(temp_audio_final_path)

    audio = AudioSegment.from_file(temp_audio_final_path)
    audio = audio + amplitude_change

    if pitch_change != 0:
        new_sample_rate = int(audio.frame_rate * (2.0 ** (pitch_change / 12.0)))
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
        audio = audio.set_frame_rate(44100)

    output_file_path = os.path.join(PROCESSED_FOLDER, "translated_output.mp3")
    output_file_final_path = data_mail_id + '/' + output_file_path
    audio.export(output_file_final_path, format="mp3")
    print(f"Audio saved to {output_file_final_path}")
    return output_file_final_path

def remove_audio(data_mail_id, input_video):
    input_stream = ffmpeg.input(input_video)
    base_name = os.path.splitext(os.path.basename(input_video))[0]
    output_video = os.path.join(PROCESSED_FOLDER, f"{base_name}_no_audio.mp4")
    output_video_save = data_mail_id + '/' + output_video
    output_stream = ffmpeg.output(input_stream, output_video_save, c='copy', an=None)
    ffmpeg.run(output_stream, overwrite_output=True)
    print(f"Output video saved to {output_video_save}")
    return output_video_save

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
    global data_usr_mail
    data_usr_mail = request.form.get('u_mail_id')  # Get the user's email
    print('nwoq2212')

    # if not data_usr_mail:
    #     return jsonify({'error': 'No email provided'}), 400
    # data_usr_mail = request.data['u_mail_id']
    # global file_save_path
    # print(data_usr_mail)
    file_save_path = data_usr_mail + '/upload/'
    os.makedirs(file_save_path, exist_ok=True)
    # file_save_path = data_usr_mail + '/download/'
    file_save_path = '/downloads/'

    os.makedirs(file_save_path, exist_ok=True)
    file_save_path = data_usr_mail + '/transcriptions/'
    os.makedirs(file_save_path, exist_ok=True)
    file_save_path = data_usr_mail + '/current/'
    os.makedirs(file_save_path, exist_ok=True)
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(file_path, "ths")
        file_save_path = data_usr_mail + '/' + file_path # data_usrmail/uploads/vid.mp4
        file.save(file_save_path)
        print()
        
        transcription_text = []

        try:
            audio_file_path = convert_mp4_to_wav(file_save_path, data_usr_mail)
            if audio_file_path is None:
                return jsonify({'error': 'Failed to convert video to audio'}), 500

            # Load audio file
            audio = AudioSegment.from_wav(audio_file_path)
            
            # Detect non-silent regions
            non_silent_regions = detect_non_silent_regions(audio) ##
            
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
                translated_audio_path = text_to_speech_from_text(data_usr_mail, translated_text, lang=dest_lang, pitch_change=0)
                translated_audio_segment = AudioSegment.from_file(translated_audio_path)
                translated_audio_segments.append((start, translated_audio_segment))
                
            final_audio = AudioSegment.silent(duration=len(audio))
            
            # Overlay translated segments back into their original positions
            for start, segment in translated_audio_segments:
                final_audio = final_audio.overlay(segment, position=start*1000)

            final_audio_path = os.path.join(PROCESSED_FOLDER, "final_translated_audio.wav")
            final_audio_save_path = data_usr_mail + '/' + final_audio_path
            final_audio.export(final_audio_save_path, format="wav")
            
            # Remove original audio from video
            silent_video_path = remove_audio(data_usr_mail, file_save_path)
            if not silent_video_path:
                return jsonify({'error': 'Failed to remove audio from video'}), 500

            # Merge new audio with silent video
            final_video_path = os.path.join(PROCESSED_FOLDER, f"{os.path.splitext(file.filename)[0]}_final.mp4")
            final_video_save_path = data_usr_mail + '/' + final_video_path
            merge_audio_with_silent_video(silent_video_path, final_audio_save_path, final_video_save_path)
            final_video_save_path = data_usr_mail + '/current/current.mp4' 
            merge_audio_with_silent_video(silent_video_path, final_audio_save_path, final_video_save_path)

            # Save the transcription to a file
            transcription_file_path = os.path.join(TRANSCRIPTIONS_FOLDER, f"{os.path.splitext(file.filename)[0]}_transcription.txt")
            transcription_final_file_path = data_usr_mail + '/' + transcription_file_path
            with open(transcription_final_file_path, "w") as f:
                for line in transcription_text:
                    f.write(line + "\n")
                    
            # Return the URL of the final video and transcription file
            #====# final_video_url = f"./{data_usr_mail}/downloads/"
            #====# transcription_file_url = f"./{data_usr_mail}/transcriptions/{os.path.basename(transcription_file_path)}"


            # @app.route('/upload/<filename>')
            # def uploaded_file(filename):
            #     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


            # @app.route('/processed/<filename>')
            # def processed_file(filename):
            #     return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

            # send_from_directory(file_save_path, filename)

            # final_video_url = f"/{data_usr_mail}/downloads/{os.path.basename(final_video_path)}"
            final_video_url = f"/downloads/{os.path.basename(final_video_path)}"

            print("================================###################++++++++++++++++++++++++++")
            print(final_video_url)
            print("================================###################++++++++++++++++++++++++++")

            transcription_file_url = f"{data_usr_mail}/transcriptions/{os.path.basename(transcription_file_path)}"
            print("================================###################++++++++++++++++++++++++++")
            print(transcription_file_url)
            print("================================###################++++++++++++++++++++++++++")
           
            return jsonify({
                'message': 'File successfully processed',
                'video_url': final_video_url,
                'transcription_url': transcription_file_url,
                'transcription': translated_text,
                'detected_language': detected_lang,
                'file_name': os.path.basename(final_video_path),
            }), 200

            # return jsonify({
            #     'message': 'File successfully processed',
            #     'video_url': final_video_url,
            #     'transcription_url': transcription_file_url,
            #     'transcription': translated_text,
            #     'detected_language': detected_lang, 
            #     'file_name' : os.path.basename(final_video_path),
            # }), 200
        
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'File not allowed'}), 400


# print(data_usr_mail)
# @app.route('/{data_usr_mail}/transcriptions/<filename>')
# def serve_transcription_file(filename):
#     return send_from_directory(file_save_path, filename)


@app.route('/transcriptions/<filename>')
def serve_transcription_file(filename):
    return send_from_directory(TRANSCRIPTIONS_FOLDER, filename)


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
    file = data['u_mail']+'/downloads'
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

# @app.route('/{data_usr_mail}/upload/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(file_save_path, filename)


# @app.route('/{data_usr_mail}/processed/<filename>')
# def processed_file(filename):
#     return send_from_directory(file_save_path, filename)

#=====================================================================

# @app.route('/upload/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# @app.route('/processed/<filename>')
# def processed_file(filename):
#     return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

#=================================================================================


# @app.route('/<user_mail>/downloads/<path:filename>')
@app.route('/downloads/<path:filename>')
def download_file(filename):
    # Construct the full path
    directory = os.path.join('/downloads/')
    return send_from_directory(directory, filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000)






#file = '../file/processed/uploads'
#os.makedirs(file, exist_ok=True)