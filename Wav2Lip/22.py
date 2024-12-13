import speech_recognition as sr
from langdetect import detect, LangDetectException
import cmudict
from collections import Counter

# Initialize CMU Pronouncing Dictionary
cmu_dict = cmudict.dict()

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_text = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except LangDetectException as e:
        print(f"Language detection error: {e}")
        return ""

def phonetic_analysis(text):
    words = text.split()
    phonetic_transcriptions = []
    for word in words:
        word_lower = word.lower()
        if word_lower in cmu_dict:
            phonetic_transcriptions.append(cmu_dict[word_lower])
        else:
            phonetic_transcriptions.append([["UNKNOWN"]])
    return phonetic_transcriptions

def analyze_accent(phonetic_transcriptions):
    # Simple heuristic rules for detecting accents
    accent_features = {
        'British': ['AH0', 'R', 'T', 'AA1'],
        'American': ['R', 'ER0', 'ER1', 'T', 'AA1', 'AE1']
    }
    
    accent_scores = {'British': 0, 'American': 0}

    for transcription in phonetic_transcriptions:
        for variant in transcription:
            for phoneme in variant:
                for accent, features in accent_features.items():
                    if phoneme in features:
                        accent_scores[accent] += 1

    # Determine the accent with the highest score
    detected_accent = max(accent_scores, key=accent_scores.get)
    return detected_accent, accent_scores

def main(file_path):
    # Transcribe the audio file
    transcribed_text = transcribe_audio(file_path)
    if transcribed_text:
        print("Transcribed Text:", transcribed_text)
        
        # Detect the language of the transcribed text
        language = detect_language(transcribed_text)
        print("Detected Language:", language)
        
        # Perform phonetic analysis
        phonetic_transcriptions = phonetic_analysis(transcribed_text)
        print("Phonetic Analysis:")
        for word, phonetics in zip(transcribed_text.split(), phonetic_transcriptions):
            print(f"{word}: {phonetics}")
        
        # Analyze accent
        detected_accent, accent_scores = analyze_accent(phonetic_transcriptions)
        print("Detected Accent:", detected_accent)
        print("Accent Scores:", accent_scores)
    else:
        print("No transcribed text available for analysis.")

# Path to your audio file
file_path = '/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/te.wav'
main(file_path)
