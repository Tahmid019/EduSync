from moviepy.editor import VideoFileClip

def convert_mp4_to_wav(mp4_file, wav_file):
    video_clip = VideoFileClip(mp4_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(wav_file)

if __name__ == "__main__":
    mp4_file_path = "engvid.mp4"
    wav_file_path = "output.wav"
    convert_mp4_to_wav(mp4_file_path, wav_file_path)
