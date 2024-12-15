import os
import subprocess

def extract_audio(video_path, audio_path):
    command = f"ffmpeg -i {video_path} -q:a 0 -map a {audio_path} -y"
    subprocess.call(command, shell=True)

if __name__ == "__main__":
    video_path = "C:/Users/maina/Downloads/bengali.mp4"
    audio_path = "C:/Users/maina/Downloads/bengali.wav"
    extract_audio(video_path, audio_path)
    print(f"Audio extracted to {audio_path}")
