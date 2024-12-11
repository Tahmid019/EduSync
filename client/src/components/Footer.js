import React from 'react'
import NavBar from '../components/NavBar'
import "../css/normalize.css"
import "../css/main.css"
import _4Dots from "../images/4-dots.jpg"
import { Link } from 'react-router-dom'


function Footer() {
  return (
    <div>
        <footer class="footer section">
                <div class="footer__container container grid">
                    <div class="footer__content grid">
                        <div class="footer__data">
                            <h3 class="footer__title">Lip-Sync</h3>
                            <p class="footer__description">Create and Customise <br />your choice ,
                                we offer you the <br /> best results.
                            </p>
                            <div>
                                <Link to="#" target="_blank" class="footer__social">
                                    <i class="ri-facebook-box-fill"></i>
                                </Link>
                                <Link to="#" target="_blank" class="footer__social">
                                    <i class="ri-twitter-fill"></i>
                                </Link>
                                <Link to="#" target="_blank" class="footer__social">
                                    <i class="ri-instagram-fill"></i>
                                </Link>
                                <Link to="#" target="_blank" class="footer__social">
                                    <i class="ri-youtube-fill"></i>
                                </Link>
                            </div>
                        </div>

                        <div class="footer__data">
                            <h3 class="footer__subtitle">Site Map</h3>
                            <ul>
                                <li class="footer__item">
                                    <Link to="" class="footer__link">About Us</Link>
                                </li>
                                <li class="footer__item">
                                    <Link to="" class="footer__link">Features</Link>
                                </li>
                                <li class="footer__item">
                                    <Link to="" class="footer__link">Demo</Link>
                                </li>
                            </ul>
                        </div>

                        <div class="footer__data">
                            <h3 class="footer__subtitle">Stay Connected</h3>
                            <ul>
                                <li class="footer__item">
                                    <Link to="" class="footer__link">Subscribe to Our Newsletter</Link>
                                </li>
                                <li class="footer__item">
                                    <Link to="" class="footer__link">Donate</Link>
                                </li>
                            </ul>
                        </div>

                        <div class="footer__data">
                            <h3 class="footer__subtitle">Support</h3>
                            <ul>
                                <li class="footer__item">
                                    <Link to="" class="footer__link">FAQs</Link>
                                </li>
                                <li class="footer__item">
                                    <Link to="" class="footer__link">Support Center</Link>
                                </li>
                                <li class="footer__item">
                                    <Link to="" class="footer__link">Contact Us</Link>
                                </li>
                            </ul>
                        </div>
                    </div>

                    <div class="footer__rights">
                        <p class="footer__copy">&#169; 2024 LipSync | All Rights Reserved</p>
                        <div class="footer__terms">
                            <Link to="#" class="footer__terms-link">Terms & Agreements</Link>
                            <Link to="#" class="footer__terms-link">Privacy Policy</Link>
                        </div>
                    </div>
                </div>
            </footer>
    </div>
  )
}

export default Footer