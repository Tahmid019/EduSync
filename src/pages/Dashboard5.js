import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

import NavBar from '../components/NavBar';
import TopNavbar from '../components/TopNavbar';
import SideBar from '../components/SideBar';

import "../css/dashboard2.css";
import "../css/transvid.css";
import "../css/TopNavbar.css";
import "../css/main.css";

import loadGif from "./videos/load-36_256.gif";
import noPhoto from "../../src/images/nophoto.095de2657a3c6d22d251.png";
import LogoHeader from "../components/svgs/Logo.svg";

function Dashboard() {
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState('');
    const [videoUrl, setVideoUrl] = useState('');
    const [srcLang, setSrcLang] = useState('en');
    const [destLang, setDestLang] = useState('bn'); // Default to Bengali
    const [loading, setLoading] = useState(false);
    const [pollInterval, setPollInterval] = useState(null); // Track polling interval ID

    // Cookie helpers
    const setCookie = (cname, cvalue, exdays) => {
        const d = new Date();
        d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
        document.cookie = `${cname}=${cvalue};expires=${d.toUTCString()};path=/`;
    };

    const getCookie = (cname) => {
        const name = `${cname}=`;
        const cookies = document.cookie.split(';');
        for (let c of cookies) {
            c = c.trim();
            if (c.startsWith(name)) {
                return c.substring(name.length);
            }
        }
        return '';
    };

    // Check user authentication on component mount
    useEffect(() => {
        const usrname = getCookie('usrname');
        if (!usrname) {
            navigate('/user');
        }
    }, [navigate]);

    const handleLogout = () => {
        setCookie('usrmail', '', -1);
        setCookie('usrpasskey', '', -1);
        setCookie('usrname', '', -1);
        navigate('/user');
    };

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        setFile(selectedFile);
        if (selectedFile) {
            setPreviewUrl(URL.createObjectURL(selectedFile));
        } else {
            setPreviewUrl('');
        }
    };

    const handleLangChange = (e) => setDestLang(e.target.value);
    const handleLangChange2 = (e) => setSrcLang(e.target.value);

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) return;

        // Stop any ongoing polling
        if (pollInterval) {
            clearInterval(pollInterval);
            setPollInterval(null);
        }

        setLoading(true);
        const utcStr = new Date().getTime(); // Unique identifier for the video file
        const formData = new FormData();
        formData.append('video', file);
        formData.append('dest_lang', destLang);
        formData.append('sr_lang', srcLang);
        formData.append('u_mail_id', getCookie('usrmail'));
        formData.append('utc_str', utcStr);

        try {
            const response = await axios.post('/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            console.log(response.data);
            setVideoUrl(''); // Clear previous video URL
            pollForFile(utcStr); // Start polling
        } catch (error) {
            console.error('Error uploading file', error);
        }
    };

    const pollForFile = (utcStr) => {
        const filename = `merged_final_video_${utcStr}.mp4`;
        console.log(`Polling for file: ${filename}`);
        const interval = setInterval(async () => {
            try {
                console.log(`Checking for file: ${filename}`);
                const response = await axios.get(`http://<backend-server>/check-file?filename=${filename}`);
                if (response.status === 200) {
                    console.log(`File found: ${filename}`);
                    setVideoUrl(`http://127.0.0.1:5001/uploads/${filename}`); // Replace with actual video URL
                    setLoading(false);
                    clearInterval(interval); // Stop polling
                    setPollInterval(null);
                }
            } catch (error) {
                // File not yet available; continue polling
            }
        }, 3000); // Poll every 3 seconds

        setPollInterval(interval);
    };

    return (
        <div>
            <div id="nav-bar">
                <div id="nav-logo">
                    <Link
                        to="/"
                        className="navbar-brand"
                        style={{
                            background: `url(${LogoHeader})`,
                            height: '60px',
                            width: '100px',
                            backgroundSize: 'contain',
                            borderRadius: '15px',
                            backgroundPosition: 'center',
                            backgroundRepeat: 'no-repeat',
                            marginTop: '-10px',
                        }}
                    ></Link>
                </div>
                <div id="logout-btn" title="logout" onClick={handleLogout}>
                    Logout
                </div>
            </div>
            <div id="main-body">
                <main>
                    <div id="sidebar">
                        <div id="user-section">
                            <div
                                id="user-logo"
                                style={{ backgroundImage: `url(${noPhoto})`, backgroundSize: 'cover' }}
                            ></div>
                            <div id="user-name">{getCookie('usrname') || 'User'}</div>
                            <div id="user-profile">Profile</div>
                        </div>
                        <div id="options">
                            <div id="trans">
                                <div id="trans-logo"></div>
                                <div id="trans-text">Translate</div>
                            </div>
                            <div id="uploaded-vid">
                                <div id="up-vid-logo"></div>
                                <div id="up-vid-logo">Uploads</div>
                            </div>
                        </div>
                    </div>
                    <div id="trans-vid">
                        <div id="up-vid">
                            <div id="upload-section">
                                {previewUrl ? (
                                    <video src={previewUrl} controls></video>
                                ) : (
                                    <div className="placeholder">Upload a video to preview</div>
                                )}
                            </div>
                            <form onSubmit={handleUpload}>
                                <div id="file-section">
                                    <select value={srcLang} onChange={handleLangChange2}>
                                        <option value="">Source Language</option>
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
                                    <select value={destLang} onChange={handleLangChange}>
                                        <option value="">Destination Language</option>
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
                                    <label htmlFor="upvid">
                                        <input type="file" id="upvid" onChange={handleFileChange} />
                                        Choose Video
                                    </label>
                                </div>
                                <button id="up-btn" type="submit">
                                    Upload
                                </button>
                            </form>
                        </div>
                        <div id="down-vid">
                            {loading ? (
                                <div id="loading">
                                    <img src={loadGif} alt="Loading..." />
                                </div>
                            ) : videoUrl ? (
                                <div id="downvid">
                                    <video src={videoUrl} controls></video>
                                    <a href={videoUrl} download>
                                        <button id="down-btn">Download</button>
                                    </a>
                                </div>
                            ) : (
                                <div className="placeholder">Processed video will appear here</div>
                            )}
                        </div>
                    </div>
                </main>
            </div>
        </div>
    );
}

export default Dashboard;
