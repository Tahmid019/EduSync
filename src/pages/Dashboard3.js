import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

import NavBar from '../components/NavBar'
import TopNavbar from '../components/TopNavbar'
import SideBar from '../components/SideBar'

import "../css/dashboard2.css";
import "../css/transvid.css";
import "../css/TopNavbar.css";
import "../css/main.css";
import upVid from "./svhi1.mp4";
import noPhoto from "../../src/images/nophoto.095de2657a3c6d22d251.png";
import LogoHeader from "../components/svgs/Logo.svg";

function Dashboard() {
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [videoUrl, setVideoUrl] = useState('');
    const [transcription, setTranscription] = useState('');
    const [destLang, setDestLang] = useState('bn'); // Default to Bengali
    const [loading, setLoading] = useState(false);

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

    const handleFileChange = (e) => setFile(e.target.files[0]);

    const handleLangChange = (e) => setDestLang(e.target.value);

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('video', file);
        formData.append('dest_lang', destLang);
        formData.append('u_mail_id', getCookie('usrmail'));
        formData.append('utc_str', new Date().getTime());

        try {
            const response = await axios.post('/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            setVideoUrl(response.data.video_url || '');
            setTranscription(response.data.transcription || 'Transcription unavailable');
        } catch (error) {
            console.error('Error uploading file', error);
            setTranscription('Error uploading file');
        } finally {
            setLoading(false);
        }
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
                                <video src={upVid} controls></video>
                            </div>
                            <form onSubmit={handleUpload}>
                                <div id="file-section">
                                    <select value={destLang} onChange={handleLangChange}>
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
                            <div id="downvid">
                                <video src={videoUrl} controls></video>
                            </div>
                            <button id="down-btn">Download</button>
                        </div>
                    </div>
                </main>
            </div>
        </div>
    );
}

export default Dashboard;
