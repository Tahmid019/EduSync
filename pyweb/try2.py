import speech_recognition as sr
import ffmpeg

def transcribe_audio(file_path):
    # Initialize recognizer class (for recognizing the speech)
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio_text = recognizer.record(source)

    try:
        # Using google speech recognition
        text = recognizer.recognize_google(audio_text)
        # print('Transcription: {}'.format(text))
        return recognizer.recognize_google(audio_text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def convert_mp4_to_wav(mp4_file_path, wav_file_path):
    # Use ffmpeg to extract audio and convert to WAV
    ffmpeg.input(mp4_file_path).output(wav_file_path, format='wav').run()




if __name__ == "__main__":
    video_file_path = "vid2.mp4"

    convert_mp4_to_wav(video_file_path, "vid2.wav")

    audio_file_path = "vid2.wav"
    # text = transcribe_audio(audio_file_path)
   
    with open("transcription.txt", "w") as file:
        file.write(transcribe_audio(audio_file_path))
