from flask import Blueprint, request, jsonify
from services.translation_service import translate_text

translation_bp = Blueprint('translation', __name__)

@translation_bp.route('/translate', methods=['POST'])
def translate_route():
    data = request.json
    text = data.get('text')
    target_language = data.get('language')
    translated_text = translate_text(text, target_language)
    return jsonify({'translated_text': translated_text})