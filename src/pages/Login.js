import React from 'react'
import NavBar from '../components/NavBar';
import "../css/login.css"
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import TopNavbar from '../components/TopNavbar';
import { Link } from 'react-router-dom';
import Footer from '../components/Footer';

function Login() {
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

  
  async function dataviewserver() {
    const dataget = await fetch('http://lipsync.in/data')
    // const dataget = await fetch('/user')
    const fulldata1 = await dataget.json();
    console.log(fulldata1)
    return fulldata1
  }

  const fulldata = dataviewserver();
  console.log(fulldata)

  const handleSubmit = async (e) => {
  };

  return (
    <div style={{ "backgroundImage": "url(../images/loginbg.jpg)", "overflowY": "hidden", "width": "100vw" }}>
      <NavBar />
      <div className="wrapper" style={{ "backgroundColor": "hsl( 190 , 64%, 22%)", }}>

        <div className="form-box">

          <form className="login-container" id="login" onSubmit={handleSubmit}>
            <div className="top">
              <span>Don't have an account?
                <Link to="/signup">Sign Up</Link></span>
              <header>Login</header>
            </div>
            <div id='define' style={{ "color": "red" }}></div>
            <div className="input-box">
              <input id='usrmail' type="text" className="input-field" placeholder="Username or Email" />
              <i className="bx bx-user"></i>
            </div>
            <div className="input-box">
              <input id='usrpass' type="password" className="input-field" placeholder="Password" />
              <i className="bx bx-lock-alt"></i>
            </div>
            <div className="input-box">
              <input type="button" className="submit" value="Sign In" onClick={
                () => {
                  async function datafromserver() {
                    const dataget = await fetch('http://lipsync.in/data')
                    // const dataget = await fetch('/user')
                    const fulldata = await dataget.json();
                    console.log(fulldata)
                    var flag = 0;
                    var umailid = document.getElementById('usrmail').value;
                    var upasscode = document.getElementById('usrpass').value;
                    var usrfullname = ''
                    if (umailid != '' && upasscode != '') {
                      for (var i = 0; flag != 1; i++) {
                        if ((umailid == fulldata[i].u_mail) && (upasscode == fulldata[i].u_pass)) {
                          flag = 1;
                          usrfullname = fulldata[i].u_fname + " " + fulldata[i].u_fname;
                          break;
                        }
                        if (flag == 1) {
                          setCookie("usrmail", umailid, 1);
                          setCookie("usrpasskey", upasscode, 1);
                          setCookie("usrname", usrfullname, 1);
                          navigate('/user/dashboard')
                        }
                        else {
                          document.getElementById('define').innerHTML = "<center><b>Invalid mail or password</b></center>"
                        }
                      }
                    }
                    else {
                      document.getElementById('define').innerHTML = "<center><b>User mail id and password can't be blank</b></center>"
                    }
                  }
                  datafromserver()
                }
              } />
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
    </div>
  )
}

export default Login