#=====app22.py=======


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



# def detect_face_in_video(video_path):
#     # Load the pre-trained Haar Cascade classifier for face detection
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     print("====detecting face=======")
#     # Open the video file
#     cap = cv2.VideoCapture(video_path)
    
#     if not cap.isOpened():
#         print("Error: Could not open video.")
#         return False

#     face_detected = False

#     while cap.isOpened():
#         # Read frame-by-frame
#         ret, frame = cap.read()

#         if not ret:
#             break

#         # Convert frame to grayscale (Haar Cascade works with grayscale images)
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # Detect faces in the frame
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#         # If faces are found, set the flag to True and break the loop
#         if len(faces) > 0:
#             face_detected = True
#             break

#     # Release the video capture object
#     cap.release()
#     return face_detected

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

def find(search, filename):
    for root, dirs, files in os.walk(search):
        if filename in files:
            print("Found file:", os.path.join(root, filename))
            return True
    print("File not found")
    return False

#====

# def detect_face_intervals(video_path):
#     video_capture = cv2.VideoCapture(video_path)
#     face_intervals = []

#     if not video_capture.isOpened():
#         print("Error: Could not open video.")
#         return []

#     frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
#     frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
#     duration = frame_count / frame_rate
#     face_detected = False
#     start_time = 0

#     while video_capture.isOpened():
#         ret, frame = video_capture.read()
#         if not ret:
#             break

#         current_time = video_capture.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # Current time in seconds
#         rgb_frame = frame[:, :, ::-1]
#         face_locations = face_recognition.face_locations(rgb_frame)

#         if face_locations and not face_detected:
#             face_detected = True
#             start_time = current_time
#         elif not face_locations and face_detected:
#             face_detected = False
#             end_time = current_time
#             face_intervals.append((start_time, end_time))

#     if face_detected:
#         end_time = duration
#         face_intervals.append((start_time, end_time))

#     video_capture.release()
#     return face_intervals



def detect_face_intervals(video_path):
    video_capture = cv2.VideoCapture(video_path)
    face_intervals = []
    no_face_intervals = []

    if not video_capture.isOpened():
        print("Error: Could not open video.")
        return [], []

    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / frame_rate
    face_detected = False
    start_time = 0

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break

        current_time = video_capture.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # Current time in seconds
        rgb_frame = frame[:, :, ::-1]
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
            continue

    if face_detected:
        face_intervals.append((start_time, duration - start_time))
    else:
        no_face_intervals.append((start_time, duration - start_time))

    video_capture.release()
    return face_intervals, no_face_intervals

def split_video(video_path, face_intervals, output_prefix):
    print("1")
    split_files = []
    print("2======>")
    try:
        for i, (start, duration) in enumerate(face_intervals):
            print(f"===={i}")
            output_path = f"{output_prefix}_face_interval_{i}.mp4"
            ffmpeg.input(video_path, ss=start, t=duration).output(output_path).run(overwrite_output=True)
            split_files.append(output_path)
        print("3")
        return split_files
    except Exception as r:
        print(f"====>>>>{e}")
    
def split_audio(audio_path, face_intervals, output_prefix):
    audio = AudioSegment.from_wav(audio_path)
    split_files = []
    for i, (start, duration) in enumerate(face_intervals):
        output_path = f"{output_prefix}_face_interval_{i}.wav"
        end = start + duration
        chunk = audio[start*1000:end*1000]  # pydub works in milliseconds
        chunk.export(output_path, format="wav")
        split_files.append(output_path)
    return split_files

def merge_audio_video(audio_path, video_path, output_path):
    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(audio_path)
    ffmpeg.output(input_video, input_audio, output_path, vcodec='copy', acodec='aac').run(overwrite_output=True)

def concatenate_videos(video_files, output_path):
    ffmpeg.concat(*[ffmpeg.input(v) for v in video_files], v=1, a=1).output(output_path).run(overwrite_output=True)



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    sr_lang = request.form.get('sr_lang')
    print("==========srLang:", sr_lang)
    dest_lang = request.form.get('dest_lang', 'bn')  # Default to Bengali if not provided
    utc_str = request.form.get('utc_str')
    print("=============", utc_str, "============")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    print(f"File saved at: {file_path}")

    print("Detecting face in video...")
    if(detect_face_in_video(file_path)):
        detected_face = "Face Available"
    else:
        detected_face = "Face Not Available"
    print(f"Face detection result: {detected_face}")

    transcription_text = []

    try:
        print("Converting video to WAV...")
        audio_file_path = convert_mp4_to_wav(file_path)
        if audio_file_path is None:
            return jsonify({'error': 'Failed to convert video to audio'}), 500
        print(f"Audio file saved at: {audio_file_path}")

        print("Loading audio file...")
        audio = AudioSegment.from_wav(audio_file_path)

        print("Detecting non-silent regions...")
        non_silent_regions = detect_non_silent_regions(audio)

        translated_audio_segments = []
        for start, end in non_silent_regions:
            chunk = audio[start*1000:end*1000]  # pydub works in milliseconds
            chunk.export("chunk.wav", format="wav")

            print("Transcribing audio chunk...")
            transcription = transcribe_audio("chunk.wav", sr_lang)
            transcription_text.append(transcription)
            if not transcription:
                print(f"Skipping chunk {start}-{end}: Failed to transcribe audio")
                translated_audio_segments.append((start, chunk))
                continue

            print("Translating transcription...")
            translated_text, detected_lang = translate_text_file(transcription, dest_lang, sr_lang)
            if not translated_text:
                print(f"Skipping chunk {start}-{end}: Failed to translate transcription")
                translated_audio_segments.append((start, chunk))
                continue

            print("Generating translated audio...")
            translated_audio_path = text_to_speech_from_text(translated_text, lang=dest_lang, pitch_change=0)
            translated_audio_segment = AudioSegment.from_file(translated_audio_path)
            translated_audio_segments.append((start, translated_audio_segment))

        final_audio = AudioSegment.silent(duration=len(audio))

        print("Overlaying translated segments...")
        for start, segment in translated_audio_segments:
            final_audio = final_audio.overlay(segment, position=start*1000)

        final_audio_path = os.path.join(PROCESSED_FOLDER, "final_translated_audio.wav")
        final_audio.export(final_audio_path, format="wav")

        print("Removing original audio from video...")
        silent_video_path = remove_audio(file_path)
        if not silent_video_path:
            return jsonify({'error': 'Failed to remove audio from video'}), 500
        

        #===============
        print("++++++++++++++++++++++detect_face_interval()")
        face_intervals = detect_face_intervals(silent_video_path)
        if not face_intervals:
            return jsonify({'error': 'No face detected in the video'}), 400

        print("++++++++++++++++++++++split()")
        face_video_files = split_video(silent_video_path, face_intervals, os.path.join(PROCESSED_FOLDER, 'face'))
        print("++++++++++++++++++++++split-----audio()")
        face_audio_files = split_audio(final_audio_path, face_intervals, os.path.join(PROCESSED_FOLDER, 'face_audio'))
        print("+_+--+-+-+-+--+-+loop")
        for video, audio in zip(face_video_files, face_audio_files):
            output_video_path = video.replace('face', 'face_lipsynced')
            subprocess.run(
                ['python', 'inference.py', '--checkpoint_path', 'checkpoints/wav2lip.pth',
                '--face', video, '--audio', audio, '--outfile', output_video_path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        print("========END LOOP")
        non_face_intervals = [(0, face_intervals[0][0])] + [(face_intervals[i][1], face_intervals[i+1][0]) for i in range(len(face_intervals) - 1)] + [(face_intervals[-1][1], int(cv2.VideoCapture(file_path).get(cv2.CAP_PROP_FRAME_COUNT)) / int(cv2.VideoCapture(file_path).get(cv2.CAP_PROP_FPS)))]
        non_face_video_files = split_video(file_path, non_face_intervals, os.path.join(PROCESSED_FOLDER, 'non_face'))
        non_face_audio_files = split_audio(audio_file_path, non_face_intervals, os.path.join(PROCESSED_FOLDER, 'non_face_audio'))
        print("                 MERGE")
        merged_video_files = []
        for non_face_video, non_face_audio in zip(non_face_video_files, non_face_audio_files):
            output_video_path = non_face_video.replace('non_face', 'merged')
            merge_audio_video(non_face_audio, non_face_video, output_video_path)
            merged_video_files.append(output_video_path)
        print("                 END")
        final_video_files = sorted(face_video_files + merged_video_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        final_output_path = os.path.join(RESULTS, f"{os.path.splitext(file.filename)[0]}_final.mp4")
        concatenate_videos(final_video_files, final_output_path)

        #=================
        # subprocess.run([
        #     'python3', 'inference.py',
        #     '--checkpoint_path', 'checkpoints/wav2lip_gan.pth',
        #     '--face', silent_video_path,
        #     '--audio', final_audio_path,
        #     '--wav2lip_batch_size', '128',
        #     '--face_det_batch_size', '4'
        # ])

        # print("Merging new audio with silent video...")
        # final_video_path = os.path.join(PROCESSED_FOLDER, f"{os.path.splitext(file.filename)[0]}_{utc_str}_final.mp4")
        # merge_audio_with_silent_video(silent_video_path, final_audio_path, final_video_path)

        print("Saving transcription to file...")
        transcription_file_path = os.path.join(TRANSCRIPTIONS_FOLDER, f"{os.path.splitext(file.filename)[0]}_{utc_str}_transcription.txt")
        with open(transcription_file_path, "w") as f:
            for line in transcription_text:
                f.write(line + "\n")

        print("Returning response...")
        # final_video_url = f"/results/result_voice.mp4"
        transcription_file_url = f"/transcriptions/{os.path.basename(transcription_file_path)}"
        
        return jsonify({
            'message': 'File successfully processed',
            'video_url': final_output_path,  #final_video_url
            'transcription_url': transcription_file_url,
            'transcription': translated_text,
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
