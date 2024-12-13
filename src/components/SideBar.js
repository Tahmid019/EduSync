import React from 'react'
import "../css/SideBar.css"
import { useState } from 'react'
import ErrorPage from '../pages/ErrorPage'
import TranslateScetion from './TranslateScetion'
import Videos from './Videos'
import "../css/main.css"
import { useNavigate } from 'react-router-dom'
import noPhoto from "../../src/images/nophoto.095de2657a3c6d22d251.png"

function SideBar(usrdetailsall) {
    const navigate = useNavigate()
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
    let usrmail = getCookie("usrmail");
    if(!usrmail) {
        navigate('/user')
    }
    const [section, setSection] = useState(<TranslateScetion />)
    // function cssReset() {
    //     document.getElementById("option-dashboard").style.backgroundColor = "#7000ff"
    //     document.getElementById("option-dashboard").style.color = "white"
    //     document.getElementById("option-uploads").style.backgroundColor = "#7000ff"
    //     document.getElementById("option-uploads").style.color = "white"
    //     document.getElementById("option-translate").style.backgroundColor = "#7000ff"
    //     document.getElementById("option-translate").style.color = "white"
    //     document.getElementById("option-gopro").style.backgroundColor = "#7000ff"
    //     document.getElementById("option-gopro").style.color = "white"
    // }
    const changeStateUploads = () => {
        // cssReset();
        // document.getElementById("option-uploads").style.backgroundColor = "#ebe3f5"
        // document.getElementById("option-uploads").style.color = "#290557"
        setSection(<Videos />)
    }
    const changeStateTranslate = () => {
        // cssReset();
        setSection(<TranslateScetion />)
    }
    const changeStateGopro = () => {
        // cssReset();
        setSection("Go Pro")
    }
    return (
        <div id='main-body'>
            <div className="sidebar">
                <img className="userIcon" src={noPhoto} alt="#" />
                <div className="userName" id='usermail'>{usrdetailsall.u_fullname || "User"}</div>
                <div className="userOptions">
                    <div id="option-uploads" onClick={
                        ()=>{
                            changeStateUploads()
                        }
                        }>Uploads</div>
                    <div id="option-translate" onClick={changeStateTranslate}>Translate</div>
                    <div id="option-gopro" onClick={changeStateGopro}>Go Pro</div>
                </div>
            </div>

            <div id="action-section">
                {section}
            </div>
        </div>
    )
}

export default SideBar