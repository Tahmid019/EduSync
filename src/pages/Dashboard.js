import React from 'react'
import NavBar from '../components/NavBar'
import TopNavbar from '../components/TopNavbar'
import SideBar from '../components/SideBar'
// import "../css/main.css"
import "../css/TopNavbar.css"
import "../css/main.css"
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

    return (
        <div onLoad={
            () => {
                if (!getCookie("usrname"))
                    navigate("/user")
            }
        }>
            <div id="dashboard-navbar">
                <div id="logo-section" onClick={homeNavigate}>
                    <Link to="/" className="navbar-brand" style={{ "background": "url(" + LogoHeader + ")", "height": "60px", "width": "100px", "backgroundSize": "contain", "borderRadius": "15px", "backgroundPosition": "center", "backgroundRepeat": "norepeat", "marginTop": "-10" }}>
                    </Link>
                </div>
                <div id="mode-change">
                    <button onClick={
                        () => {
                            setCookie("usrmail", "", -1);
                            setCookie("usrpasskey", "", -1);
                            setCookie("usrname", "User", -1);
                            navigate('/user')
                        }
                    }>Logout</button>
                </div>
            </div>
            <SideBar umail_id={usrmail} upass_key={usrpasskey} u_fullname={usrname} />
        </div>
    )
}

export default Dashboard