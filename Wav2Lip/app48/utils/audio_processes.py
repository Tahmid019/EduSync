import os
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment




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

def text_to_speech_from_text(PROCESSED_FOLDER, text, lang='bn', amplitude_change=0, pitch_change=0):
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
