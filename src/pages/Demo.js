import React, { useState } from 'react';
import NavBar from '../components/NavBar';
import { Link, useNavigate } from 'react-router-dom';
import Footer from '../components/Footer';

function Demo() {

    function setCookie(cname, cvalue, exdays) {
        const d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        let expires = "expires=" + d.toUTCString();
        document.cookie = `${cname}=${cvalue};${expires};path=/`;
    }

    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        u_mail: '',
        u_pass: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevent the default form submission behavior
        try {
            const response = await fetch('https://ipapi.co/json/');
            const data = await response.json();
            console.log('User IP:', data.ip);
            setCookie('usrip_address', data.ip, 1); // Set the IP address as a cookie with a 1-day expiration
            navigate('/demo/review');
        } catch (error) {
            console.error('Error fetching IP address:', error);
        }
    };

    return (
        <div>
            <NavBar />
            <div className="wrapper" style={{ backgroundColor: "hsl(190, 64%, 22%)" }}>
                <div className="form-box">
                    <form className="register-container" id="register" onSubmit={handleSubmit}>
                        <div className="top">
                            <span>Have an account? <Link to="/user">Login</Link></span>
                            <header>Demo</header>
                        </div>
                        <div className="input-box">
                            <input
                                id='usrmail'
                                type="text"
                                className="input-field"
                                name="u_mail"
                                value={formData.u_mail}
                                onChange={handleChange}
                                placeholder="Email"
                            />
                            <i className="bx bx-envelope"></i>
                        </div>
                        <div className="input-box">
                            <input
                                id='usrpasscode'
                                type="password"
                                className="input-field"
                                name="u_pass"
                                value={formData.u_pass}
                                onChange={handleChange}
                                placeholder="Password"
                            />
                            <i className="bx bx-lock-alt"></i>
                        </div>
                        <div className="input-box">
                            <input type="submit" className="submit" value="Register" />
                        </div>
                        <div className="two-col">
                            <div className="one">
                                <input type="checkbox" id="register-check" />
                                <label htmlFor="register-check"> Remember Me</label>
                            </div>
                            <div className="two">
                                <label><a href="#">Terms & conditions</a></label>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <Footer />
        </div>
    );
}

export default Demo;
