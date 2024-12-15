from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import speech_recognition as sr
import ffmpeg
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment, silence
from flask_cors import CORS
import mysql.connector

sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Directory setup
UPLOAD_FOLDER = 'uploads/'
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
        return recognizer.recognize_google(audio_text)
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


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    dest_lang = request.form.get('dest_lang', 'bn')  # Default to Bengali if not provided

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

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
        final_video_path = os.path.join(PROCESSED_FOLDER, f"{os.path.splitext(file.filename)[0]}_final.mp4")
        merge_audio_with_silent_video(silent_video_path, final_audio_path, final_video_path)

        # Save the transcription to a file
        transcription_file_path = os.path.join(TRANSCRIPTIONS_FOLDER, f"{os.path.splitext(file.filename)[0]}_transcription.txt")
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
            'transcription': transcription_text,
            'detected_language': detected_lang
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
    cursor.execute('CREATE TABLE IF NOT EXISTS `lipsync`.`userregdetails` (`uid` INT NOT NULL AUTO_INCREMENT , `u_fname` TEXT NOT NULL , `u_lname` TEXT NOT NULL , `u_mail` VARCHAR(90) NOT NULL , `u_pass` VARCHAR(16) NOT NULL , `u_reg_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (`uid`))')
    cursor.execute('SELECT * FROM `userregdetails`')
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(result)


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
    query = 'INSERT INTO `userregdetails` (u_fname, u_lname, u_mail, u_pass) VALUES (%s, %s, %s, %s)'
    cursor.execute(query, (data['u_fname'], data['u_lname'], data['u_mail'], data['u_pass']))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'User created successfully'}), 201


@app.route('/processed/<filename>')
def serve_processed_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
