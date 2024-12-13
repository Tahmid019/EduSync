import React from 'react'
import "../css/main.css"
import "../css/videos.css"

function Videos() {
    return (
        <div>
            <div id="container-videos">
                <div id="video-card">
                    <div id="vid-thumb">
                        <svg width="30%" height="40%" viewBox="0 0 74 98" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M36.875 85.6182C57.2405 85.6182 73.75 69.1087 73.75 48.7432C73.75 28.3777 57.2405 11.8682 36.875 11.8682C16.5095 11.8682 0 28.3777 0 48.7432C0 69.1087 16.5095 85.6182 36.875 85.6182ZM31.8877 32.3156L55.0114 45.1621C57.8213 46.7232 57.8213 50.7643 55.0114 52.3253L31.8877 65.1718C28.6106 66.9924 24.5833 64.6228 24.5833 60.8739V36.6136C24.5833 32.8647 28.6106 30.495 31.8877 32.3156Z" fill="#7000FF" fill-opacity="0.61" />
                        </svg>
                    </div>
                    <div id="vid-details">
                        <div id="vid-details-main">
                            <div id="vid-name">Video Name</div>
                            <div id="vid-lang">Hindi to Bengali</div>
                        </div>
                        <div id="vid-details-below">
                            <div id="vid-size">300 Mb</div>
                            <div id="vid-upload-date">Uploaded on 27-09-2023</div>
                            <div id="vid-feedback">★★★★★</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Videos