import React from 'react'
import "../css/normalize.css"
import "../css/main.css"
import { defer, Link } from 'react-router-dom'
import { useRef } from 'react';
import Videofile from "../components/assets/video/demo-video.mp4"
import CloseIcon from "../images/close-icon.jpg"
import _4Dots from "../images/4-dots.jpg"
import Voice from "../images/voice.jpg"
import Text from "../images/text.jpg"
import ImageJpg from "../images/image.jpg"
import Custom from "../images/custom.jpg"
import About1Img from "../images/about.jpg"
import Post2 from "../images/post-2.jpg"
import Post3 from "../images/post-3.jpg"
import Banner2 from "../images/banner-2-img.jpg"
import about1 from "../components/assets/img/about1.jpeg"
import about2 from "../components/assets/img/about2.jpeg"
import discover1 from "../components/assets/img/discover1.jpeg"
import discover2 from "../components/assets/img/discover2.jpeg"
import discover3 from "../components/assets/img/discover3.jpeg"
import discover4 from "../components/assets/img/discover4.jpeg"
import LogoHeader from "../components/svgs/logo2.svg"


function NavBar() {
    function onWindowLoad() {
        // document.body.onscroll = () => {
        //     if (document.getElementById('header-inner').scrollTop >= 100) {
        //         document.getElementById('navbar-header').style.backgroundColor = 'white'
        //     }
        //     if (document.getElementById('header-inner').scrollTop <= 100) {
        //         document.getElementById('navbar-header').style.backgroundColor = 'white'
        //     }
        // }
        const navbarShowBtn = document.querySelector('.navbar-show-btn');
        const navbarCollapseDiv = document.querySelector('.navbar-collapse');
        const navbarHideBtn = document.querySelector('.navbar-hide-btn');

        if (navbarShowBtn && navbarCollapseDiv && navbarHideBtn) {
            navbarShowBtn.onclick = function () {
                navbarCollapseDiv.classList.add('navbar-show');
            };

            navbarHideBtn.onclick = function () {
                navbarCollapseDiv.classList.remove('navbar-show');
            };
        } else {
            console.error('Navbar elements not found');
        }

        function changeSearchIcon() {
            const searchIconImg = document.querySelector('.search-icon img');
            if (searchIconImg) {
                let winSize = window.matchMedia("(min-width: 1200px)");
                if (winSize.matches) {
                    searchIconImg.src = "images/search-icon.png";
                } else {
                    searchIconImg.src = "images/search-icon-dark.png";
                }
            } else {
                console.error('Search icon image not found');
            }
        }

        window.onresize = function () {
            changeSearchIcon();
            document.body.classList.add('resize-animation-stopper');
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function () {
                document.body.classList.remove('resize-animation-stopper');
            }, 400);
        };

        changeSearchIcon();

        let resizeTimer;

        /*==================== VIDEO ====================*/
        const videoFile = document.getElementById('video-file'),
            videoButton = document.getElementById('video-button'),
            videoIcon = document.getElementById('video-icon')

        function playPause() {
            if (videoFile.paused) {
                // Play video
                videoFile.play()
                // We change the icon
                videoIcon.classList.add('ri-pause-line')
                videoIcon.classList.remove('ri-play-line')
            }
            else {
                // Pause video
                videoFile.pause();
                // We change the icon
                videoIcon.classList.remove('ri-pause-line')
                videoIcon.classList.add('ri-play-line')

            }
        }

        function finalVideo() {
            // Video ends, icon change
            videoIcon.classList.remove('ri-pause-line')
            videoIcon.classList.add('ri-play-line')
        }



        // function scrollHeader() {
        //     const header = document.getElementById('header')
        //     // When the scroll is greater than 100 viewport height, add the scroll-header class to the header tag
        //     if (this.scrollY >= 100) header.style.backgroundColor = "white !important"; else header.classList.remove('scroll-header')
        // }
        // document.body.onscroll = () => {
        //     scrollHeader()
        // }

    }
    return (
        <div>
            <nav className="navbar" id='navbar-header'>
                    <div className="container flex">
                    <Link to="/" className="navbar-brand">
                        <img 
                            src={LogoHeader} 
                            alt="Logo" 
                            style={{
                                height: "60px",
                                width: "100px",
                                borderRadius: "15px",
                                objectFit: "contain",
                                marginTop: "-10px",
                            }} 
                        />
                    </Link>
                        <button type="button" className="navbar-show-btn" onClick={onWindowLoad}>
                            <i className="ri-function-line" style={{ "color": "var(--light-color)" }}></i>
                        </button>

                        <menu className="navbar-collapse bg-white">
                            <button type="button" className="navbar-hide-btn">
                                <img src={CloseIcon} />
                            </button>
                            <ul className="navbar-nav">
                                <li className="nav-item">
                                    <Link to="/" className="nav-link">Home</Link>
                                </li>
                                <li className="nav-item">
                                    <Link to="/#about" className="nav-link">About</Link>
                                </li>
                                <li className="nav-item">
                                    <Link to="/#discover" className="nav-link">Service</Link>
                                </li>
                                <li className="nav-item">
                                    <Link to="/#demo" className="nav-link">Demo</Link>
                                </li>
                                <li className="nav-item">
                                    <Link to="/ourteam" className="nav-link">Our Team</Link>
                                </li>
                                <li className="nav-item">
                                    <Link to="/#contact" className="nav-link">Contact</Link>
                                </li>
                                <li className="nav-item">
                                    <Link to="/user" className="nav-link">Sign In</Link>
                                </li>
                            </ul>
                            <div className="nav__dark" onClick={() => {
                                const themeButton = document.getElementById('theme-button')
                                const darkTheme = 'dark-theme'
                                const iconTheme = 'ri-sun-line'

                                // Previously selected topic (if user selected)
                                const selectedTheme = localStorage.getItem('selected-theme')
                                const selectedIcon = localStorage.getItem('selected-icon')

                                // We obtain the current theme that the interface has by validating the dark-theme class
                                const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light'
                                const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'ri-moon-line' :
                                    'ri-sun-line'

                                // We validate if the user previously chose a topic
                                if (selectedTheme) {
                                    // If the validation is fulfilled, we ask what the issue was to know if we activated or
                                    document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme)
                                    themeButton.classList[selectedIcon === 'ri-moon-line' ? 'add' : 'remove'](iconTheme)
                                }

                                // Activate / deactivate the theme manually with the button
                                themeButton.onclick = function () {
                                    // Add or remove the dark / icon theme
                                    document.body.classList.toggle(darkTheme)
                                    themeButton.classList.toggle(iconTheme)
                                    // We save the theme and the current icon that the user chose
                                    localStorage.setItem('selected-theme', getCurrentTheme())
                                    localStorage.setItem('selected-icon', getCurrentIcon())
                                }

                            }
                            }>
                                <i className="ri-moon-line change-theme" id="theme-button"></i>
                            </div>
                            <div className="nav__toggle" id="nav-toggle">
                                <i className="ri-function-line"></i>
                            </div>
                        </menu>
                    </div>
                </nav>
        </div>
    )
}

export default NavBar