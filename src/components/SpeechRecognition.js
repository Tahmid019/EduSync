// src/SpeechToText.js
import React, { useState } from 'react';

const SpeechToText = () => {
  const [transcript, setTranscript] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [error, setError] = useState('');

  const handleStart = () => {
    setIsListening(true);
    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
      const transcriptText = event.results[0][0].transcript;
      setTranscript(transcriptText);
      setIsListening(false);
    };

    recognition.onerror = (event) => {
      setError(`Error occurred in recognition: ${event.error}`);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  return (
    <div>
      <h1>Speech to Text Transcription</h1>
      <button onClick={handleStart} disabled={isListening}>
        {isListening ? 'Listening...' : 'Start Transcription'}
      </button>
      {transcript && (
        <div>
          <h2>Transcription:</h2>
          <p>{transcript}</p>
        </div>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default SpeechToText;
