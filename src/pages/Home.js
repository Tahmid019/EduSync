import React from 'react'
import NavBar from '../components/NavBar'
// import "../css/normalize.css"
// import "../css/main.css"
import { defer, Link } from 'react-router-dom'
import { useRef } from 'react';
// import "../js/script.js"
import HomeBg from "../components/images/HomePage_bg2.jpeg"
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

function Home() {
    // document.body.onscroll = () => {
    //     function scrollUp() {
    //         const scrollUp = document.getElementById('scroll-up');
    //         // When the scroll is higher than 200 viewport height, add the show-scroll class to the a tag with the scroll-top class
    //         if (window.scrollY >= 200) scrollUp.classList.add('show-scroll');
    //         else scrollUp.classList.remove('show-scroll')
    //     }
    //     const sections = document.querySelectorAll('section[id]')
    //     function scrollActive() {
    //         const scrollY = window.pageYOffset

    //         sections.forEach(current => {
    //             const sectionHeight = current.offsetHeight
    //             const sectionTop = current.offsetTop - 50;
    //             const sectionId = current.getAttribute('id')

    //             if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
    //                 document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.add('active-link')
    //             } else {
    //                 document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.remove('active-link')
    //             }
    //         })
    //     }
    //     /*==================== SHOW MENU ====================*/
    //     const navMenu = document.getElementById('nav-menu'),
    //         navToggle = document.getElementById('nav-toggle'),
    //         navClose = document.getElementById('nav-close')

    //     /*===== MENU SHOW =====*/
    //     /* Validate if constant exists */
    //     if (navToggle) {
    //         navToggle.onclick = function () {
    //             navMenu.classList.add('show-menu');
    //         }
    //     }

    //     /*===== MENU HIDDEN =====*/
    //     /* Validate if constant exists */
    //     if (navClose) {
    //         navClose.onclick = function () {
    //             navMenu.classList.remove('show-menu');
    //         }
    //     }

    //     /*==================== REMOVE MENU MOBILE ====================*/
    //     const navLink = document.querySelectorAll('.nav__link')

    //     function linkAction() {
    //         const navMenu = document.getElementById('nav-menu')
    //         // When we click on each nav__link, we remove the show-menu class
    //         navMenu.classList.remove('show-menu')
    //     }
    //     navLink.forEach(n => n.onclick = linkAction)

    //     /*==================== CHANGE BACKGROUND HEADER ====================*/
    //     function scrollHeader() {
    //         const header = document.getElementById('header')
    //         // When the scroll is greater than 100 viewport height, add the scroll-header class to the header tag
    //         if (window.scrollY >= 100) header.classList.add('scroll-header');
    //         else header.classList.remove('scroll-header')
    //     }
    //     window.onscroll = function () {
    //         scrollHeader();
    //         scrollUp();
    //         scrollActive();
    //     }
    // }

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
        videoButton.addEventListener('click', playPause)

        document.getElementById('video-button').onclick = playPause

        function finalVideo() {
            // Video ends, icon change
            videoIcon.classList.remove('ri-pause-line')
            videoIcon.classList.add('ri-play-line')
        }
        // ended, when the video ends
        videoFile.addEventListener('ended', finalVideo)



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
            <header className="header bg-blue" style={{ backgroundImage: `url(${HomeBg})`, "backgroundSize": "cover", "backgroundPosition":"right" , "width":"-webkit-fill-available"}}>

                <nav className="navbar" id='navbar-header'>
                    <div className="container flex">
                        <Link to="/" className="navbar-brand" style={{"background" : "url("+LogoHeader+")", "height":"60px", "width":"60px", "backgroundSize":"cover", "borderRadius":"0px", "backgroundPosition":"center", "backgroundRepeat":"norepeat", "marginTop":"-10",}}>
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
                                    <a href="#" className="nav-link">Home</a>
                                </li>
                                <li className="nav-item">
                                    <a href="#about" className="nav-link">About</a>
                                </li>
                                <li className="nav-item">
                                    <a href="#discover" className="nav-link">Service</a>
                                </li>
                                <li className="nav-item">
                                    <a href="#demo" className="nav-link">Demo</a>
                                </li>
                                <li className="nav-item">
                                    <Link to="/ourteam" className="nav-link">Our Team</Link>
                                </li>
                                <li className="nav-item">
                                    <a href="#contact" className="nav-link">Contact</a>
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

                <div className="header-inner text-white text-center">
                    <div className="container grid">
                        <div className="header-inner-left">
                            <div class="home__data">
                                <br />
                                <span class="home__data-subtitle">Deep Learning AI</span>
                                <h1 class="home__data-title">Explore <br /><b> Lip-Sync AI</b><br />All-in-one<br />Translation Model</h1><br/>
                                <a href="#about" class="button" style={{"fontSize":"20px"}}>Explore</a>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            <main>
                <section className="about section" id="about">
                    <div className="about__container container grid">
                        <div className="about__data">
                            <h2 className="section__title about__title">About <br /> Lip-Sync</h2>
                            <p className="about__description">Welcome to LipSync, where we harness the power of deep
                                learning AI to deliver precise and culturally nuanced language translations.
                                Our neural networks ensure accurate translations, helping businesses and
                                individuals communicate seamlessly across borders. Experience the future of
                                translation with our innovative solutions, designed to break language barriers
                                and enhance global connectivity.
                            </p>
                            <Link to="/demo" className="button">Explore more?</Link>
                        </div>

                        <div className="about__img">
                            <div
                                className="about__img-overlay"
                                style={{
                                    width: "-webkit-fill-available",
                                    height: "300px",
                                    backgroundImage: `url(${About1Img})`, 
                                    backgroundSize: "contain",
                                    backgroundRepeat: "no-repeat",
                                    backgroundPosition: "center"
                                }}
                            >
                            </div>
                        </div>
                    </div>
                </section>

                <section className="discover section" id="discover">
                    <section id="services" className="services py">
                        <div className="container">
                            <div className="section-head text-center">
                                <h2 className="lead">Discover the most <br /> attractive Features</h2>
                                <p className="text text-lg">A perfect way to show your services</p>
                                <div className="line-art flex">
                                    <div></div>
                                    <img src={_4Dots} />
                                    <div></div>
                                </div>
                            </div>
                            <div className="services-inner text-center grid">
                                <article className="service-item">
                                    <div className="icon">
                                        <img src={Voice} />
                                    </div>
                                    <h3>Voice Translation</h3>
                                    <p className="text text-sm">Discover seamless voice translation on our website, enabling users to
                                        translate spoken words instantly with accuracy and natural fluency. Powered by advanced deep
                                        learning AI, our platform facilitates effortless communication across languages, enhancing
                                        global connectivity for users worldwide. </p>
                                </article>

                                <article className="service-item">
                                    <div className="icon">
                                        <img src={ImageJpg} />
                                    </div>
                                    <h3>Lip-Syncing</h3>
                                    <p className="text text-sm">Experience flawless lip-syncing on our site, where translated speech
                                        seamlessly matches natural lip movements. Powered by advanced technology, our platform
                                        ensures authentic communication across languages in any context.</p>
                                </article>

                                <article className="service-item">
                                    <div className="icon">
                                        <img src={Text} />
                                    </div>
                                    <h3>Text-to-Speech</h3>
                                    <p className="text text-sm">TTS technology enables screen readers to audibly read aloud the content
                                        of the website to users who are visually impaired or blind. This includes text on web pages,
                                        as well as navigation menus, form fields, and other interactive elements, allowing users to
                                        navigate and access information effectively.</p>
                                </article>

                                <article className="service-item">
                                    <div className="icon">
                                        <img src={Custom} />
                                    </div>
                                    <h3>Customizable Interfaces</h3>
                                    <p className="text text-sm">It empowers individuals to tailor their browsing experience to their
                                        unique needs and preferences, improving accessibility and inclusivity on the website. It's
                                        essential to gather feedback from users throughout the design and development process to
                                        ensure that the customization options meet their specific needs and preferences effectively.
                                    </p>
                                </article>
                            </div>
                        </div>
                    </section>
                </section>

                <section className="video section" id="demo">
                    <h2 className="section__title">Demo Video</h2>

                    <div className="video__container container">
                        <p className="video__description">Find out more with our Demo video of our work.
                        </p>

                        <div className="video__content">
                            <video id="video-file" src={Videofile}>
                                <source src={Videofile} type="video/mp4" />
                            </video>

                            <button className="button button--flex video__button" id="video-button" onClick={
                                () => {
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

                                    playPause()

                                    function finalVideo() {
                                        // Video ends, icon change
                                        videoIcon.classList.remove('ri-pause-line')
                                        videoIcon.classList.add('ri-play-line')
                                    }
                                    videoFile.addEventListener('ended', finalVideo)
                                }
                            }>
                                <i className="ri-play-line video__button-icon" id="video-icon"></i>
                            </button>
                        </div>
                    </div>
                </section>

                <section className="review section">
                    <h2 className="section__title">Lip-Sync <br /> Live Review</h2>
                    <div className="review_container" id="review">
                        <div className="feedback" id="feedback-card">
                            <div id="review-stars">★★★★★</div>
                            <div id="review-text">The features are good, its well translated but need some refinement
                            </div>
                            <div id="review-user-details">
                                <div id="review-user-img"></div>
                                <div id="review-user-name">User Name</div>
                                <div id="review-date">30.05.2024</div>
                            </div>
                        </div>
                        <div className="feedback" id="feedback-card">
                            <div id="review-stars">★★★★★</div>
                            <div id="review-text">The features are good, its well translated but need some refinement
                            </div>
                            <div id="review-user-details">
                                <div id="review-user-img"></div>
                                <div id="review-user-name">User Name</div>
                                <div id="review-date">30.05.2024</div>
                            </div>
                        </div>
                        <div className="feedback" id="feedback-card">
                            <div id="review-stars">★★★★★</div>
                            <div id="review-text">The features are good, its well translated but need some refinement
                            </div>
                            <div id="review-user-details">
                                <div id="review-user-img"></div>
                                <div id="review-user-name">User Name</div>
                                <div id="review-date">30.05.2024</div>
                            </div>
                        </div>
                    </div>
                </section>

                <section id="contact" className="contact py">
                    <div className="container grid">
                        <div className="contact-left">
                            <iframe src="https://maps.google.com/maps/embed?pb=?cid=9362887102108936347&entry=gps"
                                width="600" height="450" style={{ "border": "0" }} allowfullscreen=""
                                loading="lazy"></iframe>
                        </div>
                        <div className="contact-right text-white text-center">
                            <div className="contact-head">
                                <h3 className="lead">Contact Us</h3>
                                <p className="text text-md">-------------------</p>
                            </div>
                            <form>
                                <div className="form-element">
                                    <input type="text" className="form-control" placeholder="Your name" />
                                </div>
                                <div className="form-element">
                                    <input type="email" className="form-control" placeholder="Your email" />
                                </div>
                                <div className="form-element">
                                    <textarea rows="5" placeholder="Your Message" className="form-control"></textarea>
                                </div>
                                <button type="submit" className="btn btn-white btn-submit">
                                    <i className="fas fa-arrow-right"></i> Send Message
                                </button>
                            </form>
                        </div>
                    </div>
                </section>
            </main>

            <footer class="footer section">
                <div class="footer__container container grid">
                    <div class="footer__content grid">
                        <div class="footer__data">
                            <h3 class="footer__title">Lip-Sync</h3>
                            <p class="footer__description">Create and Customise <br />your choice ,
                                we offer you the <br /> best results.
                            </p>
                            <div>
                                <a href="#" target="_blank" class="footer__social">
                                    <i class="ri-facebook-box-fill"></i>
                                </a>
                                <a href="#" target="_blank" class="footer__social">
                                    <i class="ri-twitter-fill"></i>
                                </a>
                                <a href="#" target="_blank" class="footer__social">
                                    <i class="ri-instagram-fill"></i>
                                </a>
                                <a href="#" target="_blank" class="footer__social">
                                    <i class="ri-youtube-fill"></i>
                                </a>
                            </div>
                        </div>

                        <div class="footer__data">
                            <h3 class="footer__subtitle">Site Map</h3>
                            <ul>
                                <li class="footer__item">
                                    <a href="" class="footer__link">About Us</a>
                                </li>
                                <li class="footer__item">
                                    <a href="" class="footer__link">Features</a>
                                </li>
                                <li class="footer__item">
                                    <a href="" class="footer__link">Demo</a>
                                </li>
                            </ul>
                        </div>

                        <div class="footer__data">
                            <h3 class="footer__subtitle">Stay Connected</h3>
                            <ul>
                                <li class="footer__item">
                                    <a href="" class="footer__link">Subscribe to Our Newsletter</a>
                                </li>
                                <li class="footer__item">
                                    <a href="" class="footer__link">Donate</a>
                                </li>
                            </ul>
                        </div>

                        <div class="footer__data">
                            <h3 class="footer__subtitle">Support</h3>
                            <ul>
                                <li class="footer__item">
                                    <a href="" class="footer__link">FAQs</a>
                                </li>
                                <li class="footer__item">
                                    <a href="" class="footer__link">Support Center</a>
                                </li>
                                <li class="footer__item">
                                    <a href="" class="footer__link">Contact Us</a>
                                </li>
                            </ul>
                        </div>
                    </div>

                    <div class="footer__rights">
                        <p class="footer__copy">&#169; 2024 LipSync | All Rights Reserved</p>
                        <div class="footer__terms">
                            <a href="#" class="footer__terms-link">Terms & Agreements</a>
                            <a href="#" class="footer__terms-link">Privacy Policy</a>
                        </div>
                    </div>
                </div>
            </footer>
            <a href="#" className="scrollup" id="scroll-up">
                <i className="ri-arrow-up-line scrollup__icon"></i>
            </a>
            <script src="js/script.js"></script>
        </div>
    )
}

export default Home