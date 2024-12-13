// import React, { useState } from 'react';
// import axios from 'axios';
// import "../css/VideoUpload.css";

// function VidUp() {
//   const [file, setFile] = useState(null);
//   const [videoUrl, setVideoUrl] = useState('');
//   const [transcription, setTranscription] = useState('');

//   const handleFileChange = (e) => {
//     setFile(e.target.files[0]);
//   };

//   const handleUpload = async (e) => {
//     e.preventDefault();
//     if (!file) return;

//     const formData = new FormData();
//     formData.append('video', file);

//     try {
//       const response = await axios.post('/upload', formData, {
//         headers: {
//           'Content-Type': 'multipart/form-data',
//         },
//       });

//       const videoUrl = response.data.video_url;
//       const transcription = response.data.transcription || 'Transcription unavailable';

//       setVideoUrl(videoUrl);
//       setTranscription(transcription);
//     } catch (error) {
//       console.error('Error uploading file', error);
//       setTranscription('Error uploading file');
//     }
//   };

//   return (
//     <div id="App">
//       <form onSubmit={handleUpload}>
//         <input type="file" accept="video/*" onChange={handleFileChange} />
//         <button type="submit">Upload</button>
//       </form>
//       {transcription && <p>Transcription: {transcription}</p>}
//       {videoUrl && <video src={videoUrl} controls />}
//     </div>
//   );
// }

// export default VidUp;



//=================================================================================================


import React, { useState } from 'react';
import axios from 'axios';
import "../css/VideoUpload.css";
// import { stringify } from 'querystring';
// import { io } from "socket.io-client";

// import ViD from "../md.59mbl@gmail.com/downloads/bengali_final.mp4"

function VidUp() {

  var utc = new Date()
  var utc_str = String(utc.getUTCDate()) + String(utc.getUTCMonth()) + String(utc.getUTCFullYear()) + String(utc.getUTCMilliseconds()) + String(utc.getUTCSeconds()) 
   
  console.log(utc_str)

  const [file, setFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState('');
  const [transcription, setTranscription] = useState('');
  const [destLang, setDestLang] = useState('bn'); // Default to Bengali
  const [loading, setLoading] = useState(false);
  

  function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        document.getElementById("")
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

  const usrmailid = getCookie('usrmail')

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
    formData.append('dest_lang', destLang); // Add destination language to formData
    formData.append('u_mail_id', usrmailid);
    formData.append('utc_str', utc_str)

    setTimeout(() => {
      console.log("timeout")
    }, 10*60*1000)

    try {
      const response = await axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        // timeout: 300000,
      })
      


      const videoUrl = response.data.video_url;
      console.log("==========>>>>>>>" + videoUrl + "<<<<<<<===========")
      const transcription = response.data.transcription || 'Transcription unavailable';
      // const detected_face = response.data.detetcted_face
      console.log("+++++")
      // console.log(detected_face)
      console.log("========")
      

      console.log("+++++++")
      console.log(videoUrl)

      setVideoUrl(videoUrl);
      setTranscription(transcription);
    } catch (error) {
      console.error('Error uploading file', error);
      setTranscription('Error uploading file');
    } finally {
      setLoading(false);
    }

    // const selectVid = document.querySelector('#vid-area');
    // const inputFile = document.querySelector('#up');

    // selectVid.addEventListener('click', function(){
    //   inputFile.click()
    // })

    // inputFile.addEventListener('change', function() {
    //   const reader = new FileReader();
    //   reader.onload = ()=> {
    //     const vidUrl = reader.result;
    //   }
    //   reader.readAsDataURL(videoUrl)
    // })

  //   window.onload = function () {
  //     const socket = io();
  //     let socketid = undefined
  //     socket.connect("https://127.0.0.1:5000");
  //     let progressBar = document.getElementById("progressBar");

  //     socket.on("connect", function () {
  //         console.log("Connected!");
  //         socketid = socket.id;
  //         console.log("ID: " + socketid);
  //     })
  //     socket.on("update progress", function(perecent) {
  //         //do something with percent
  //         console.log("Got perecent: " + perecent);
  //         progressBar.style.width = perecent + "%";
  //     })

  //     let mainForm = document.getElementById("mainForm");
  //     mainForm.onsubmit = function(event) {
  //         event.preventDefault();
  //         fetch("/progress/" + socketid, {
  //             method: "POST"
  //         }).then(response => {
  //             setTimeout(function() {
  //                 progressBar.style.width = "0%";
  //             }, 1000);
  //         });
  //     }
  // }
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
              {/* Add more options as needed */}
            </select>
            <button id="upload-button"type="submit">Upload</button>
          </div>
        </div>
      </form>
      {loading && <p>Uploading, please wait...</p>}
      <div id="download">
        {transcription && <p>Transcription: {transcription}</p>}
        {videoUrl && <video src={videoUrl} controls />}
      </div>
      {/* <div id="progrss-bar">
        <form id = "mainForm" method="POST">
            <h1 style = "text-align: center;">Progress!</h1>
            <div style = "display: flex; justify-content: center;">
                <div class="progress" style = "width: 50vw; margin-top: 10px; margin-right: 1vw; background-color: grey;">
                    <div class="progress-bar" id = "progressBar" role="progressbar" aria-label="Basic example" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </div>
        </form>
          </div> */}
    </div>
  );
}

export default VidUp;

