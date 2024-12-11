import os
import subprocess
import librosa
import numpy as np
import joblib

def extract_audio(video_path, audio_path):
    command = f"ffmpeg -i {video_path} -q:a 0 -map a {audio_path} -y"
    subprocess.call(command, shell=True)

def extract_features(audio_path):
    y, sr = librosa.load(audio_path)
    pitch, _ = librosa.piptrack(y=y, sr=sr)
    pitches = pitch[pitch > 0]
    median_pitch = np.median(pitches)
    return median_pitch

def classify_gender(features):
    model = joblib.load('gender_classifier.pkl')  # Ensure this file exists
    features = np.array(features).reshape(1, -1)  # Ensure features are in the correct shape
    prediction = model.predict(features)
    return 'male' if prediction[0] == 1 else 'female'

def main(video_path):
    audio_path = 'extracted_audio.wav'
    extract_audio(video_path, audio_path)
    features = extract_features(audio_path)
    gender = classify_gender(features)
    os.remove(audio_path)
    return gender

if __name__ == "__main__":
    video_path = 'path_to_your_video.mp4'
    gender = main(video_path)
    print(f"The detected voice is: {gender}")
