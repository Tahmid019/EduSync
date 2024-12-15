from flask import Flask, request, jsonify
import mysql.connector
import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr

# from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# app.config.from_object(Config)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lipsync'

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="lipsync"
# )

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
            video = VideoFileClip(file_path)
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_audio.wav')
            video.audio.write_audiofile(audio_path)

            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
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
    
    file = '../'+data['u_mail']+'/uploads'
    os.makedirs(file, exist_ok=True)
    file = '../'+data['u_mail']+'/processed'
    os.makedirs(file, exist_ok=True)

    mydb = mysql.connector.connect(host="localhost", user="root", password="")
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