import speech_recognition as sr

def transcribe_audio(file_path, sr_lang, retries=3):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_text = recognizer.record(source)
    
    attempt = 0
    while attempt < retries:
        try:
            text = recognizer.recognize_google(audio_text, language=sr_lang)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            return ""
        except sr.RequestError as e:
            print(f"Attempt {attempt+1}: Could not request results from Google Speech Recognition service; {e}")
            attempt += 1
    return "Request failed after multiple attempts"

file_path = '/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/te.wav'
sr_lang = 'te-IN'

text = transcribe_audio(file_path, sr_lang)
print(text)
# from langdetect import detect, LangDetectException

# def transcribe_audio(file_path):
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(file_path) as source:
#         audio_text = recognizer.record(source)
#     try:
#         text = recognizer.recognize_google(audio_text)
#         # text2 = recognizer.recognize_wit(audio_text)
#         return text
#     except sr.UnknownValueError:
#         print("Google Speech Recognition could not understand the audio")
#         return ""
#     except sr.RequestError as e:
#         print(f"Could not request results from Google Speech Recognition service; {e}")
#         return ""
    
    
# def detect_language(text):
#     try:
#         lang = detect(text)
#         return lang
#     except LangDetectException as e:
#         print(f"Language detection error: {e}")
#         return ""    
    
    
# file_path = '/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/te.wav'
# sr_lang = 'te-IN'

# text = transcribe_audio(file_path)
# print(text)
# print(detect_language(text))


# # import json
# # from ibm_watson import SpeechToTextV1
# # from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# # def transcribe_ibm(audio_path):
# #     authenticator = IAMAuthenticator('your_api_key')
# #     speech_to_text = SpeechToTextV1(authenticator=authenticator)
# #     speech_to_text.set_service_url('your_service_url')

# #     with open(audio_path, 'rb') as audio_file:
# #         result = speech_to_text.recognize(
# #             audio=audio_file,
# #             content_type='audio/wav'
# #         ).get_result()

# #     transcript = result['results'][0]['alternatives'][0]['transcript']
# #     print("Transcript: ", transcript)

# # # Example usage
# # audio_file_path = "path/to/your/audiofile.wav"
# # transcribe_ibm(audio_file_path)

