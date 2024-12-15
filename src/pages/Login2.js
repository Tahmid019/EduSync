import React, { useState, useEffect } from 'react';
import NavBar from '../components/NavBar';
import "../css/login.css";
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import Footer from '../components/Footer';

function Login() {
    const navigate = useNavigate();

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

    if(getCookie("usrmail")){
        
    }

    const handleLogin = async () => {
        try {
            const response = await fetch('/login', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(formData),
            });
      
            if (response.ok) {
              const result = await response.json();
              console.log('Server response:', result); // Log the server response to console
              navigate('/user');
            } else {
              console.error('Error sending data:', await response.text());
            }
          } catch (error) {
            console.error('Error:', error);
          }
        try {
            const response = await fetch('/data');
            const fulldata = await response.json();
            // console.log(fulldata);

            const umailid = document.getElementById('usrmail').value;
            const upasscode = document.getElementById('usrpass').value;
            
            if (umailid !== '' && upasscode !== '') {
                let flag = false;
                let usrfullname = '';

                for (const user of fulldata) {
                    if (umailid == user[3] && upasscode == user[4]) {
                        flag = true;
                        usrfullname = user[1] + " " + user[2];
                        break;
                    }
                }

                if (flag) {
                    setCookie("usrmail", umailid, 1);
                    setCookie("usrpasskey", upasscode, 1);
                    setCookie("usrname", usrfullname, 1);
                    navigate('/user/dashboard');
                } else {
                    document.getElementById('define').innerHTML = "<center><b>Invalid mail or password</b></center>";
                }
            } else {
                document.getElementById('define').innerHTML = "<center><b>User mail id and password can't be blank</b></center>";
            }
        } catch (error) {
            console.error('Error during login:', error);
            document.getElementById('define').innerHTML = "<center><b>Server error, please try again later</b></center>";
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        handleLogin();
    };

    return (
        <div style={{ backgroundImage: "url(../images/loginbg.jpg)", overflowY: "hidden", width: "100vw" }}>
            <NavBar />
            <div className="wrapper" style={{ backgroundColor: "hsl(190, 64%, 22%)" }}>
                <div className="form-box">
                    <form className="login-container" id="login" onSubmit={handleSubmit}>
                        <div className="top">
                            <span>Don't have an account? <Link to="/signup">Sign Up</Link></span>
                            <header>Login</header>
                        </div>
                        <div id='define' style={{ color: "red" }}></div>
                        <div className="input-box">
                            <input id='usrmail' type="text" className="input-field" placeholder="Username or Email" />
                            <i className="bx bx-user"></i>
                        </div>
                        <div className="input-box">
                            <input id='usrpass' type="password" className="input-field" placeholder="Password" />
                            <i className="bx bx-lock-alt"></i>
                        </div>
                        <div className="input-box">
                            <input type="submit" className="submit" value="Sign In" />
                        </div>
                        <div className="two-col">
                            <div className="one">
                                <input type="checkbox" id="login-check" />
                                <label> Remember Me</label>
                            </div>
                            <div className="two">
                                <label><a href="#">Forgot password?</a></label>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <Footer />
        </div>
    );
}
export default Login;
