from flask import Flask
import os
from flask_cors import CORS

from routes.audio import audio_bp
from routes.translation import translation_bp

import locale
locale.getpreferredencoding = lambda: "UTF-8"

app = Flask(__name__)
CORS(app)

#load configuration
app.config.from_pyfile('config/settings.py')

#creating required directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
os.makedirs(app.config['TRANSCRIPTIONS_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS'], exist_ok=True)

#register blueprints
app.register_blueprint(audio_bp, url_prefix='/api/audio')
app.register_blueprint(translation_bp, url_prefix='/api/translation')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
