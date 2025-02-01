import React from 'react';
import '../css/abt_styles.css';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
import { Link, useNavigate } from 'react-router-dom';

function abt() {
    return (
        <div>
            <NavBar />
            <main className="main">
                <section className="teacher section" id="teacher">
                    <div id="container-mentoreos">
                        <div id="mentoreo-card">
                            <div id="mentor-thumb1"></div>
                            <div id="mentor-details">
                                <div id="mentor-details-main">
                                    <div id="mentor-name">Dr. Partha Pakray</div>
                                    <div id="mentor-lang">Associate Professor, National Institute of Technology Silchar (Govt. of India)</div>
                                    <div id="mentor-gsid">Google Scholar : H-Index-21</div>
                                    {/* <a href="tel:+917005321897"><div id="mentor-mob">Phone : (+91) 7005 321 894</div></a> */}
                                    <a href="mailto:parthapakray@gmail.com"><div id="mentor-mail">Email : parthapakray@gmail.com</div></a>
                                </div>
                            </div>
                            
                        </div>

                        <div id="mentoreo-card">
                            <div id="mentor-thumb2"></div>
                            <div id="mentor-details">
                                <div id="mentor-details-main">
                                    <div id="mentor-name">Dr. Sivaji Bandyopadhyay</div>
                                    <div id="mentor-lang">Professor,  Jadavpur University</div>
                                    <div id="mentor-gsid">Google Scholar : H-Index-46</div>
                                    {/* <a href="tel:+917005321897"><div id="mentor-mob">Phone : (+91) 7005 321 894</div></a> */}
                                    <a href="mailto:sivaji.bandyopadhyay@jadavpuruniversity.in"><div id="mentor-mail">Email : sivaji.bandyopadhyay@jadavpuruniversity.in</div></a>
                                </div>
                            </div>
                            
                        </div>
                    </div>
                </section>

                <section className="teams section" id="teams">

                    <div id="team-details">
                        <div id="team1-cards">
                            <div id="cards-a">
                               
                                <div id="card2">
                                    <div id="tm-img">
                                        <div id="tahmid"></div>
                                    </div>
                                    <div id="tm-fd">
                                        <div id="tm-name">Tahmid Choudhary</div>
                                        <div id="tm-about">UG 2nd Year</div>
                                        <div id="tm-work-at">NIT Silchar</div>
                                    </div>
                                    <div id="tm-social">
                                        <span id="mail-logo" onClick={()=>{window.location.href = 'mailto:tahmidchoudhury.dev@gmail.com'}}>
                                            <a href="">
                                                <mail width="512" height="512" />
                                            </a>
                                        </span>
                                        <span id="lin-logo" onClick={()=>{window.location.href = 'https://www.linkedin.com/in/tahmid-choudhury-513a4a28b'}}>
                                            <a href="">
                                                <lin width="512" height="512" />
                                            </a>
                                        </span>
                                        <span id="git-logo" onClick={()=>{window.location.href = 'https://github.com/Tahmid019'}}><a href="">
                                            <git width="512" height="512" />
                                        </a>
                                        </span>
                                    </div>
                                </div>
                            </div>
                            
                        </div>
                        <div id="team1-works">
                            <div id="team-no">Team 1</div>
                            <div id="team-works-details">
                                Team 1 is an enthusiastic and diverse team of 2nd-year college students dedicated to breaking down language barriers, trying to develop LipSync, a language translation website aimed at providing accurate and real-time translation services for text, voice and video content.
                            </div>
                        </div>
                    </div>
                    
                    <Footer />
                </section>
            </main>
        </div>
    )
}

export default abt