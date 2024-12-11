import requests
import time


api_key = "10535479a2da4344aeb172ac69453d6e"
headers = {
    "authorization": api_key,
    "content-type": "application/json"
}


def upload_file(file_path):
    upload_url = "https://api.assemblyai.com/v2/upload"
    with open(file_path, 'rb') as file:
        response = requests.post(upload_url, headers=headers, files={"file": file})
    response.raise_for_status()
    return response.json()['upload_url']


def transcribe_audio(audio_url):
    transcribe_url = "https://api.assemblyai.com/v2/transcript"
    json_data = {
        "audio_url": audio_url
    }
    response = requests.post(transcribe_url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()['id']


def get_transcription_result(transcription_id):
    result_url = f"https://api.assemblyai.com/v2/transcript/{transcription_id}"
    while True:
        response = requests.get(result_url, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result['status'] == 'completed':
            return result['text']
        elif result['status'] == 'failed':
            raise Exception("Transcription failed")
        else:
            time.sleep(5) 


audio_path = "aud1.mp3"
try:
    audio_url = upload_file(audio_path)
    # "https://youtube.com/shorts/7wqpsYMuiNs?si=0bYWKAPAF3BW6WWz"
    transcription_id = transcribe_audio(audio_url)
    transcription_text = get_transcription_result(transcription_id)
    print(transcription_text)

    with open("transcription.txt", 'w') as file:
        file.write(transcription_text)
except Exception as e:
    print(f"An error occurred: {e}")
