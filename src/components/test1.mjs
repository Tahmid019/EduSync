const fs = require('fs');
const fetch = require('node-fetch');

const apiKey = "10535479a2da4344aeb172ac69453d6e";
const headers = {
    "authorization": apiKey,
    "content-type": "application/json"
};

async function uploadFile(filePath) {
    const uploadUrl = "https://api.assemblyai.com/v2/upload";
    const fileStream = fs.createReadStream(filePath);

    const response = await fetch(uploadUrl, {
        method: 'POST',
        headers: {
            "authorization": apiKey
        },
        body: fileStream
    });

    if (!response.ok) {
        throw new Error(`Failed to upload file: ${response.statusText}`);
    }

    const data = await response.json();
    return data.upload_url;
}

async function transcribeAudio(audioUrl) {
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
}

async function getTranscriptionResult(transcriptionId) {
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
}

async function main() {
    const audioPath = "aud1.mp3";

    try {
        const audioUrl = await uploadFile(audioPath);
        const transcriptionId = await transcribeAudio(audioUrl);
        const transcriptionText = await getTranscriptionResult(transcriptionId);
        console.log(transcriptionText);

        fs.writeFileSync("transcription.txt", transcriptionText);
    } catch (error) {
        console.error(`An error occurred: ${error.message}`);
    }
}

main();
