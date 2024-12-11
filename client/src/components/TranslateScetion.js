import React from 'react'
// import UploadVidNoVid from './UploadVidNoVid'
import "../css/translate.css"
// import TestUpload from './TestUpload'
// import TryUpload from './TryUpload'
// import VideoUpload from './VideoUpload.mjs'
import VidUp from './VidUp.js'
// import SpeechToText from './SpeechRecognition'
// import SpeechToText from './FileExtract'
import "../css/VideoUpload.css";

function TranslateScetion() {
    return (
        <div>
            <div id="translate-section">
                <div id="upload-video">
                    <VidUp />
                </div>
            </div>
            <div id="translate-btn-section"></div>
        </div>
    )
}

export default TranslateScetion