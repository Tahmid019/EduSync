import React, { useState } from 'react';
import axios from 'axios';
import "../css/VideoUpload.css"

const VideoUpload = () => {
  const [file, setFile] = useState(null);
  const [transcription, setTranscription] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('video', file);

    try {
      const response = await axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('File uploaded successfully', response.data);
      setTranscription(response.data.transcription);
    } catch (error) {
      console.error('Error uploading file', error);
      setTranscription('Error uploading file');
    }
  };

  return (
    <div >
      <form onSubmit={handleSubmit}>
        <input type="file" accept="video/mp4" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {transcription && (
        <div>
          <h2>Transcription:</h2>
          <p>{transcription}</p>
        </div>
      )}
    </div>
  );
};

export default VideoUpload;