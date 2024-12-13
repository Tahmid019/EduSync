// src/SpeechToText.js
import React, { useState } from 'react';
import axios from 'axios';

const SpeechToText = () => {
  const [transcript, setTranscript] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleTranscription = async () => {
    if (!file) {
      setError('Please upload an audio file first.');
      return;
    }

    setIsProcessing(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('audio', file);

      const response = await axios.post('https://api.assemblyai.com/v2/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setTranscript(response.data.transcript);
      setIsProcessing(false);
    } catch (e) {
      setError(`Error processing file: ${e.message}`);
      setIsProcessing(false);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([transcript], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'transcripted.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div>
      <h1>Audio to Text Transcription</h1>
      <input type="file" accept="audio/*" onChange={handleFileChange} />
      <button onClick={handleTranscription} disabled={isProcessing}>
        {isProcessing ? 'Processing...' : 'Start Transcription'}
      </button>
      {transcript && (
        <div>
          <h2>Transcription:</h2>
          <pre>{transcript}</pre>
          <button onClick={handleDownload}>Download Transcript</button>
        </div>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default SpeechToText;
