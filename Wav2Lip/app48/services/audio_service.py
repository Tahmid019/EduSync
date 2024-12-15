from pydub import AudioSegment

def process_audio(audio_path):
    audio = AudioSegment.from_wav(audio_path)
    return {"status": "success", "message": "Audio processed successfully"}, 