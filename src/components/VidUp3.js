import React, { useState, useEffect } from 'react';
import axios from 'axios';
import "../css/VideoUpload.css";

function VidUp() {
  const [file, setFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState('');
  const [transcription, setTranscription] = useState('');
  const [destLang, setDestLang] = useState('bn'); // Default to Bengali
  const [loading, setLoading] = useState(false);
  const [fallback, setFallback] = useState(false);
  
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleLangChange = (e) => {
    setDestLang(e.target.value);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append('video', file);
    formData.append('dest_lang', destLang);

    try {
      const response = await axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 600000,
      });

      if (response.status === 500) {
        setFallback(true);
        setTranscription('Fallback process started. Please wait...');
        pollForCompletion();
      } else {
        const videoUrl = response.data.video_url;
        const transcription = response.data.transcription || 'Transcription unavailable';
        setVideoUrl(videoUrl);
        setTranscription(transcription);
      }
    } catch (error) {
      console.error('Error uploading file', error);
      setTranscription('Error uploading file');
    } finally {
      setLoading(false);
    }
  };

  const pollForCompletion = async () => {
    const pollInterval = 5000; // Poll every 5 seconds
    const poll = setInterval(async () => {
      try {
        const response = await axios.get('/check-completion');
        if (response.data.complete) {
          clearInterval(poll);
          setVideoUrl(response.data.video_url);
          setTranscription(response.data.transcription || 'Transcription unavailable');
          setFallback(false);
        }
      } catch (error) {
        console.error('Error checking completion status', error);
      }
    }, pollInterval);
  };

  return (
    <div id="App">
      <form onSubmit={handleUpload}>
        <div id="container">
          <div id="vid-area">
            <i className='bx bxs-cloud-upload icon'/>
            <h3>Upload Video</h3>
            <p>mp4 Select Language</p>
            <input id="up" type="file" accept="video/*" onChange={handleFileChange} />
          </div>
          <div id="button">
            <select id="language-button" value={destLang} onChange={handleLangChange}>
              <option value="en">English</option>
              <option value="bn">Bengali</option>
              <option value="hi">Hindi</option>
              <option value="ta">Tamil</option>
              <option value="as">Assamese</option>
              <option value="gu">Gujarati</option>
              <option value="te">Telegu</option>
              <option value="or">Odia</option>
              <option value="kn">Kannada</option>
              <option value="pa">Punjabi</option>
              <option value="ml">Malayalam</option>
              <option value="mr">Marathi</option>
              <option value="zh">Chinese</option>
            </select>
            <button id="upload-button" type="submit">Upload</button>
          </div>
        </div>
      </form>
      {loading && <p>Uploading, please wait...</p>}
      {fallback && <p>Fallback process started, please wait...</p>}
      <div id="download">
        {transcription && <p>Transcription: {transcription}</p>}
        {videoUrl && <video src={videoUrl} controls />}
      </div>
    </div>
  );
}

export default VidUp;
