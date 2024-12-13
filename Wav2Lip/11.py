from google.cloud import speech




def transcribe_and_detect_accent(file_path):
    client = speech.SpeechClient()

    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
        model="default"
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))
        # Note: Google Cloud doesn't provide direct accent information.
        # However, additional metadata might be extracted based on regions and languages.
        print("Language Code: {}".format(result.language_code))

file_path = '/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/te.wav'
transcribe_and_detect_accent(file_path)
