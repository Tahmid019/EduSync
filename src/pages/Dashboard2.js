import React, { useState } from 'react'
import axios from 'axios';
import NavBar from '../components/NavBar'
import TopNavbar from '../components/TopNavbar'
import SideBar from '../components/SideBar'
import "../css/dashboard2.css"
import "../css/main.css"
import "../css/TopNavbar.css"
import "../css/main.css"
import noPhoto from "../../src/images/nophoto.095de2657a3c6d22d251.png"
import LogoHeader from "../components/svgs/Logo.svg"
import { useNavigate, Link } from 'react-router-dom'


function Dashboard() {
    const navigate = useNavigate()
    function setCookie(cname, cvalue, exdays) {
        const d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        let expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }
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

    const homeNavigate = (x) => {
        navigate("/")
    }

    var usrmail = getCookie("usrmail");
    var usrpasskey = getCookie("usrpasskey");
    var usrname = getCookie("usrname");

    document.onload = () => {
        if (getCookie("usrname"))
            navigate("/user")
    }
    if (usrname == "User")
        navigate('/user')


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
        }, 10 * 60 * 1000)

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
    }

    document.onload = ()=>{
        if (!getCookie("usrname"))
            navigate("/user")
    }

    if (!getCookie("usrname"))
        navigate("/user")

    return (
        <div onLoad={
            () => {
                if (!getCookie("usrname"))
                    navigate("/user")
            }
        }>
            <div id="nav-bar">
                <div id="nav-logo">
                    <Link to="/" className="navbar-brand" style={{ "background": "url(" + LogoHeader + ")", "height": "60px", "width": "100px", "backgroundSize": "contain", "borderRadius": "15px", "backgroundPosition": "center", "backgroundRepeat": "norepeat", "marginTop": "-10" }}>
                    </Link>
                </div>
                <div id="logout-btn" title="logout" onClick={
                        () => {
                            setCookie("usrmail", "", -1);
                            setCookie("usrpasskey", "", -1);
                            setCookie("usrname", "User", -1);
                            navigate('/user')
                        }
                    }></div>
            </div>
            <main>
                <div id="sidebar">
                    <div id="user-section">
                        <div id="user-logo" style={{'backgroundImage': 'url(' + noPhoto + ')', 'backgroundSize': 'cover'}}></div>
                        <div id="user-name">{usrname || 'User'}</div>
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
                <div id="content-main">
                    <div id="trans-vid">
                        <div id="upload"></div>
                        <div id="download"></div>
                        <div id="App">
                            <form onSubmit={handleUpload}>
                                <div id="container">
                                    <div id="vid-area">
                                        <i className='bx bxs-cloud-upload icon' />
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
                                        <button id="upload-button" type="submit">Upload</button>
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
                    </div>
                </div>
            </main>
        </div>
    )
}

export default Dashboard