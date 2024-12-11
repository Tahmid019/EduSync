import React from 'react'
import "../css/TopNavbar.css"
import "../css/main.css"
import LogoHeader from "../components/svgs/Logo.svg"
import { useNavigate, Link } from 'react-router-dom'

function TopNavbar() {
    const navigate = useNavigate();
    const homeNavigate = () => {
        navigate("/")
    }
    return (
        <div>
            <div id="dashboard-navbar">
                <div id="logo-section" onClick={homeNavigate}>
                    <Link to="/" className="navbar-brand" style={{ "background": "url(" + LogoHeader + ")", "height": "60px", "width": "100px", "backgroundSize": "contain", "borderRadius": "15px", "backgroundPosition": "center", "backgroundRepeat": "norepeat", "marginTop": "-10" }}>
                    </Link>
                </div>
                <div id="mode-change"></div>
            </div>
        </div>
    )
}

export default TopNavbar