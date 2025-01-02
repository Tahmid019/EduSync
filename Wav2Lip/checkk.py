
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
from moviepy import VideoFileClip, concatenate_videoclips
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

VIDEO_DIRECTORY = '/home/oem/LIPSYNC/reactdb_new_try/reactdb_Main/reactdb/server/Wav2Lip/processed/'


@app.route('/check-file', methods=['GET'])
def check_file():
    print(f"[[==>{request.args.get('filename')}<=== ]]")
    filename = request.args.get('filename')
    # filename = 'merged_final_video_1734749218900.mp4'
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
    app.run(debug=True, port=5001)