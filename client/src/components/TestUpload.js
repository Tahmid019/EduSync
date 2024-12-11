import { AssemblyAI } from 'assemblyai';
import React, { useState } from 'react';
import { Upload, Button } from "antd";

function TestUpload(props) {
    const apiKey = "10535479a2da4344aeb172ac69453d6e";
    const headers = {
        "authorization": apiKey,
        "content-type": "application/json"
    };

    const [file, setFile] = useState(null);
    const [transcription, setTranscription] = useState(null);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const uploadFile = async (file) => {
        const uploadUrl = "https://api.assemblyai.com/v2/upload";
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(uploadUrl, {
            method: 'POST',
            headers: {
                "authorization": apiKey
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Failed to upload file: ${response.statusText}`);
        }

        const data = await response.json();
        return data.upload_url;
    };

    const transcribeAudio = async (audioUrl) => {
        const transcribeUrl = "https://api.assemblyai.com/v2/transcript";
        const jsonData = {
            "audio_url": audioUrl
        };

        const response = await fetch(transcribeUrl, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(jsonData)
        });

        if (!response.ok) {
            throw new Error(`Failed to transcribe audio: ${response.statusText}`);
        }

        const data = await response.json();
        return data.id;
    };

    const getTranscriptionResult = async (transcriptionId) => {
        const resultUrl = `https://api.assemblyai.com/v2/transcript/${transcriptionId}`;

        while (true) {
            const response = await fetch(resultUrl, {
                method: 'GET',
                headers: headers
            });

            if (!response.ok) {
                throw new Error(`Failed to get transcription result: ${response.statusText}`);
            }

            const result = await response.json();

            if (result.status === 'completed') {
                return result.text;
            } else if (result.status === 'failed') {
                throw new Error("Transcription failed");
            } else {
                await new Promise(resolve => setTimeout(resolve, 5000));
            }
        }
    };

    const handleTranscription = async () => {
        console.log("TranscriptionText")
        try {
            const audioUrl = await uploadFile(file);
            const transcriptionId = await transcribeAudio(audioUrl);
            const transcriptionText = await getTranscriptionResult(transcriptionId);
            console.log(transcriptionText)
            setTranscription(transcriptionText);
        } catch (error) {
            console.error(`An error occurred: ${error.message}`);
        }
    };


    // const videoInput = document.getElementById('videoInput');
    //     videoInput.addEventListener('change', handleFileSelect);

    // function handleFileSelect(event) {
    //     document.getElementById('action').innerHTML = '<video id="myVideo" controls autoplay></video>'
    //     const selectedFile = event.target.files[0];
    //     if (selectedFile) {
    //         // Read the file using FileReader
    //         const reader = new FileReader();
    //         reader.onload = function (e) {
    //             const videoUrl = e.target.result;
    //             // Now you can use the videoUrl to display or manipulate the video
    //             // For example, set it as the source for an HTML5 video element
    //             const videoElement = document.getElementById('myVideo');
    //             videoElement.src = videoUrl;
    //         };
    //         reader.readAsDataURL(selectedFile);
    //     }
    // }

    return (
        <div className="action">
            <input type="file" id="videoInput" accept="video/*" onChange={
                function handleFileSelect(event) {
                    const selectedFile = event.target.files[0];
                    if (selectedFile) {
                        var FILE_URL;
                        const reader = new FileReader();
                        reader.onload = function (e) {
                            const videoUrl = e.target.result;
                            const videoElement = document.getElementById('myVideo');
                            videoElement.src = videoUrl;
                        };
                        reader.readAsDataURL(selectedFile);
                    }

                    //   const FILE_URL =
                    //     'https://storage.googleapis.com/aai-web-samples/5_common_sports_injuries.mp3';

                    // You can also transcribe a local file by passing in a file path
                    // const FILE_URL = './path/to/file.mp3';

                }
            } />

            <video id="myVideo" controls autoplay></video>
            <h1>Audio Transcription</h1>
            <input type="file" accept="audio/*" onChange={handleFileChange} />
            <button onClick={handleTranscription} disabled={!file}>Transcribe</button>
            { 
                <div>
                    <h2>Transcription Result:</h2>
                    <pre>{(transcription)?transcription:'Loading'}</pre>
                </div>
            }
        </div>
    )
}

export default TestUpload