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
                            <div id="mentor-thumb"></div>
                            <div id="mentor-details">
                                <div id="mentor-details-main">
                                    <div id="mentor-name">Dr. Partha Pakray</div>
                                    <div id="mentor-lang">Associate Professor, National Institute of Technology Silchar (Govt. of India)</div>
                                    <div id="mentor-gsid">Google Scholar : H-Index-21</div>
                                    <a href="tel:+917005321897"><div id="mentor-mob">Phone : (+91) 7005 321 894</div></a>
                                    <a href="mailto:parthapakray@gmail.com"><div id="mentor-mail">Email : parthapakray@gmail.com</div></a>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <section className="teams section" id="teams">

                    <div id="team-details">
                        <div id="team1-cards">
                            <div id="cards-a">
                                <div id="card1">
                                    <div id="tm-img">
                                        <div id="mainak"></div>
                                    </div>
                                    <div id="tm-fd">
                                        <div id="tm-name">Mainak Das</div>
                                        <div id="tm-about">UG 2nd Year</div>
                                        <div id="tm-work-at">NIT Silchar</div>
                                    </div>
                                    <div id="tm-social">
                                        <span id="mail-logo" onClick={()=>{window.location.href = 'mailto:mainakdas.dev@gmail.com'}}>
                                            <a href="mailto:mainakdas.dev@gmail.com">
                                                <mail width="512" height="512" />
                                            </a>
                                        </span>
                                        <span id="lin-logo" onClick={()=>{window.location.href = 'https://www.linkedin.com/in/mainakdasnits'}}>
                                            <a href="">
                                                <lin width="512" height="512" />
                                            </a>
                                        </span>
                                        <span id="git-logo" onClick={()=>{window.location.href = 'https://github.com/tech-hunter-mainak/'}}><a href="">
                                            <git width="512" height="512" />
                                        </a>
                                        </span>
                                    </div>
                                </div>
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
                            <div id="cards-b">
                                <div id="card3">
                                    <div id="tm-img">
                                        <div id="surajit"></div>
                                    </div>
                                    <div id="tm-fd">
                                        <div id="tm-name">Surajit Sutradhar</div>
                                        <div id="tm-about">UG 2nd Year</div>
                                        <div id="tm-work-at">NIT Silchar</div>
                                    </div>
                                    <div id="tm-social">
                                        <span id="mail-logo" onClick={()=>{window.location.href = 'mailto:surajit.sutradhar.11b.13@gmail.com'}}>
                                            <a href="">
                                                <mail width="512" height="512" />
                                            </a>
                                        </span>
                                        <span id="lin-logo" onClick={()=>{window.location.href = 'https://www.linkedin.com/in/surajit-sutradhar-baa14b292'}}>
                                            <a href="">
                                                <lin width="512" height="512" />
                                            </a>
                                        </span>
                                        <span id="git-logo" onClick={()=>{window.location.href = 'https://github.com/surajit-13-sutradhar'}}><a href="">
                                            <git width="512" height="512" />
                                        </a>
                                        </span>
                                    </div>
                                </div>
                                <div id="card4">
                                    <div id="tm-img">
                                        <div id="tanbir"></div>
                                    </div>
                                    <div id="tm-fd">
                                        <div id="tm-name">Tanbir Laskar</div>
                                        <div id="tm-about">UG 2nd Year</div>
                                        <div id="tm-work-at">NIT Silchar</div>
                                    </div>
                                    <div id="tm-social">
                                        <span id="mail-logo" onClick={()=>{window.location.href = 'mailto:tanbir100000@gmail.com'}}>
                                            <a href="">
                                                <mail width="512" height="512" />
                                            </a>
                                        </span>
                                        <span id="lin-logo" onClick={()=>{window.location.href = 'https://www.linkedin.com/in/tanbir-lasker-41a62728b/'}}>
                                            <a href="">
                                                <lin width="512" height="512" />
                                            </a>
                                        </span>
                                        <span id="git-logo" onClick={()=>{window.location.href = 'https://github.com/judgeofmyown'}}><a href="">
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
                    </div><div id="team-details">
                        <div id="team1-cards">
                            <div id="cards-a">
                                <div id="card1">
                                    <div id="tm-img">
                                        <div id="priyanshu"></div>
                                    </div>
                                    <div id="tm-fd">
                                        <div id="tm-name">Priyanshu Jha</div>
                                        <div id="tm-about">UG 4th Year</div>
                                        <div id="tm-work-at">NIT Silchar</div>
                                    </div>
                                    <div id="tm-social">
                                        <span id="mail-logo" onClick={()=>{window.location.href = 'mailto:priyanshujha21_ug@ece.nits.ac.in'}}>
                                            <a href="">
                                                <mail width="512" height="512" />
                                            </a>
                                        </span>
                                        <span id="lin-logo" onClick={()=>{window.location.href = 'https://www.linkedin.com/in/priyanshujha120302?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BC1mGi02KRSKxNWEAXyEs5w%3D%3D'}}>
                                            <a href="">
                                                <lin width="512" height="512" />
                                            </a>
                                        </span>
                                        <span id="git-logo" onClick={()=>{
                                            window.location.href =''
                                        }}></span>
                                    </div>
                                </div>
                                <div id="card2">
                                    <div id="tm-img">
                                        <div id="ayan"></div>
                                    </div>
                                    <div id="tm-fd">
                                        <div id="tm-name">Ayanangshu Das Majumdar</div>
                                        <div id="tm-about">UG 4th Year</div>
                                        <div id="tm-work-at">NIT Silchar</div>
                                    </div>
                                    <div id="tm-social">
                                        <span id="mail-logo" onClick={()=>{window.location.href = 'mailto:ayanangshuarls@gmail.com'}}>
                                            <a href="">
                                                <mail width="512" height="512" />
                                            </a>
                                        </span>
                                        <span id="lin-logo" onClick={()=>{window.location.href = 'https://www.linkedin.com/in/ayanangshu-das-majumder-b84248234?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3Bf1nM10CXQdmF%2BmZWXRHa2A%3D%3D'}}>
                                            <a href="">
                                            </a>
                                        </span>
                                        <span id="git-logo" onClick={()=>{window.location.href = ''}}><a href="#"></a>
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div id="cards-b">
                                <div id="card3">
                                    <div id="tm-img">
                                        <div id="dipan"></div>
                                    </div>
                                    <div id="tm-fd">
                                        <div id="tm-name">Dipan Patgiri</div>
                                        <div id="tm-about">UG 4th Year</div>
                                        <div id="tm-work-at">NIT Silchar</div>
                                    </div>
                                    <div id="tm-social">
                                        <span id="mail-logo" onClick={()=>{window.location.href = 'mailto:dipan21_ug@cse.nits.ac.in'}}>
                                            <a href="">
                                            </a>
                                        </span>
                                        <span id="lin-logo" onClick={()=>{window.location.href = 'https://www.linkedin.com/in/dipan-patgiri-a04473148?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BKhPpsUhUQj6iIlKnrsEiKQ%3D%3D'}}>
                                            <a href="">
                                            </a>
                                        </span>
                                        <span id="git-logo" onClick={()=>{window.location.href = ''}}><a href="#">

                                        </a>
                                        </span>
                                    </div>
                                </div>
                                <div id="card4">
                                    <div id="tm-img">
                                        <div id="protoy"></div>
                                    </div>
                                    <div id="tm-fd">
                                        <div id="tm-name">Protoy Debroy</div>
                                        <div id="tm-about">UG 4th Year</div>
                                        <div id="tm-work-at">NIT Silchar</div>
                                    </div>
                                    <div id="tm-social">
                                        <span id="mail-logo" onClick={()=>{window.location.href = 'mailto:protoy21_ug@ece.nits.ac.in'}}>
                                            <a href="">
                                                <mail width="512" height="512" />
                                            </a>
                                        </span>
                                        <span id="lin-logo" onClick={()=>{window.location.href = 'https://www.linkedin.com/in/protoy-debroy-593561256?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3Bhyud0vtKQiS31fk7Oditlg%3D%3D'}}>
                                            <a href="">
                                                <lin width="512" height="512" />
                                            </a>
                                        </span>
                                        <span id="git-logo" onClick={()=>{window.location.href = ''}}>
                                            <a href="#">
                                                <git />
                                            </a>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div id="team1-works">
                            <div id="team-no">Team 2</div>
                            <div id="team-works-details">
                                Comprises of 4th year students. A dynamic group of 4 innovative students specializing in various fiels of computer science and engineering. Their project aims to enhance user experience in applications ranging from video translation to multi-lingual connectivity.
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