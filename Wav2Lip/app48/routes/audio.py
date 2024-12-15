
from flask import Blueprint, request, jsonify
from services.audio_service import process_audio

audio_bp = Blueprint('audio', __name__)

@audio_bp.route('/process_audio', methods=['POST'])
def process_audio_route():
    data = request.get_json()
    response = process_audio(data)
    return jsonify(response)