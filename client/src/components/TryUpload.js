import React, { useState } from 'react';
// import fetch from 'node-fetch';

//--

const apiKey = "10535479a2da4344aeb172ac69453d6e";
const headers = {
    "authorization": apiKey,
    "content-type": "application/json"
};

const TryUpload = () => {
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

    return (
        <div>
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
    );
};

export default TryUpload;
