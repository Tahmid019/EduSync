import React, { useState } from 'react';
import axios from 'axios';
import "../css/VideoUpload.css";

function VidUp() {
  const [file, setFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState('');
  const [transcription, setTranscription] = useState('');
  const [destLang, setDestLang] = useState('bn'); // Default to Bengali
  const [loading, setLoading] = useState(false);
  const [srLang, setSrLang] = useState('en'); // Default to English

  function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) === ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) === 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

  const usrmailid = getCookie('usrmail');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleLangChange = (e) => {
    setDestLang(e.target.value);
  };

  const handleLangChange2 = (e) => {
    setSrLang(e.target.value);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append('video', file);
    formData.append('dest_lang', destLang);
    formData.append('sr_lang', srLang);
    formData.append('u_mail_id', usrmailid);
    formData.append('utc_str', new Date().toISOString());

    try {
      const response = await axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setVideoUrl(response.data.video_url);
      setTranscription(response.data.transcription || 'Transcription unavailable');
    } catch (error) {
      if (error.response) {
        console.error('Server responded with an error:', error.response.status, error.response.data);
        setTranscription('Server error: ' + error.response.status);
      } else if (error.request) {
        console.error('No response received:', error.request);
        setTranscription('No response received from server');
      } else {
        console.error('Error', error.message);
        setTranscription('Error: ' + error.message);
      }
    } finally {
      setLoading(false);
    }
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
            <select id="language-button" value={srLang} onChange={handleLangChange2}>
              <option value="en">English</option>
              <option value="bn">Bengali</option>
              <option value="hi">Hindi</option>
              <option value="ta">Tamil</option>
              <option value="ne">Nepali</option>
              <option value="gu">Gujarati</option>
              <option value="te">Telegu</option>
              <option value="or">Odia</option>
              <option value="kn">Kannada</option>
              <option value="pa">Punjabi</option>
              <option value="ml">Malayalam</option>
              <option value="mr">Marathi</option>
              {/* Add more options as needed */}
            </select>
            <br/>
            <select id="language-button" value={destLang} onChange={handleLangChange}>
              <option value="en">English</option>
              <option value="bn">Bengali</option>
              <option value="hi">Hindi</option>
              <option value="ta">Tamil</option>
              <option value="ne">Nepali</option>
              <option value="gu">Gujarati</option>
              <option value="te">Telegu</option>
              <option value="or">Odia</option>
              <option value="kn">Kannada</option>
              <option value="pa">Punjabi</option>
              <option value="ml">Malayalam</option>
              <option value="mr">Marathi</option>
              <option value="zh">Chinese</option>
              {/* Add more options as needed */}
            </select>
            <button id="upload-button" type="submit">Upload</button>
          </div>
        </div>
      </form>
      {loading && <p>Uploading, please wait...</p>}
      <div id="download">
        {transcription && <p>Transcription: {transcription}</p>}
        {videoUrl && <video src={videoUrl} controls />}
      </div>
    </div>
  );
}

export default VidUp;
